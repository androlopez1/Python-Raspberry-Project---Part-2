#!/usr/bin/python
import os
import time
from time import sleep, strftime, time 
from datetime import datetime
import smtplib
from email import Encoders
from email.MIMEBase import MIMEBase
from email.mime.multipart import MIMEMultipart
import sys
import Adafruit_DHT
import lcddriver
import csv

f_time = datetime.now().strftime('%a %d %b @ %H:%M')
toaddr = EMAIL HERE    # redacted
me = 'sensor@test.com' # redacted
subject = 'Data ' + f_time

msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = me
msg['To'] = toaddr
msg.preamble = "Data @ " + f_time

display = lcddriver.lcd()

while True:
  msg.set_payload([])
  humidity, temperature = Adafruit_DHT.read_retry(11, 17)
  print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
  display.lcd_display_string("Temperatura: "+str(temperature), 1)
  display.lcd_display_string("Humedad: "+str(humidity), 2)
  doc = open("data.csv","a")
  with doc:
    fieldnames = ['hora', 'temperatura','humedad']
    writer = csv.DictWriter(doc, fieldnames=fieldnames)
    writer.writerows([{'hora':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'temperatura':str(temperature),'humedad':str(humidity)}])
  doc.close()
  sleep(60)
  current_time = datetime.now()
  if ((current_time.hour == 18  and current_time.minute == 00) or (current_time.hour == 23  and current_time.minute == 59) or (current_time.hour == 6 and current_time.minute == 00) or (current_time.hour == 11 and current_time.minute == 59)):
      try:
         data = MIMEBase('application',"octect-stream")
         data.set_payload(open('data.csv').read())
         Encoders.encode_base64(data)
         data.add_header('Content-Disposition','data',filename=os.path.split("data_2.csv")[1])
         msg.attach(data)
         s = smtplib.SMTP("smtp.gmail.com", 587)
         s.starttls()
         s.login(user = 'YOUR EMAIL HERE', password = 'YOUR PASSWORD HERE')
         s.sendmail(me, toaddr, msg.as_string())
         s.quit()
         os.remove("data.csv")

      except:
         print ("Error: unable to send email")
  else:
    pass
