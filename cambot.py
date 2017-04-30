#!/usr/bin/python
import os
import datetime
from astral import Astral
import time
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from getpass import getpass

fromemail = str(raw_input("Please input outgoing email address (gmail only): "))
frompass = str(getpass(prompt="Please input the password for the outgoing email account: "))
toemail1 = str(raw_input("Please input the incomming email address: "))
toemail2 = str(raw_input("Please input the incomming email address again: "))
if toemail1 == toemail2:
    toemail = toemail1
else:
    print('The "To email" addresses do not match. Exiting.')
    exit()

image_cmd = "fswebcam -r 1920x1080 --crop 1080x1080[480,0] --no-banner upload-image.jpg"
city_name = "Boston"
a = Astral()
city = a[city_name]
current_date = datetime.date.today()
sunrise = city.sun(date=current_date, local=True)['sunrise'].replace(tzinfo=None)
did_upload = False

def send_email():
    msg = MIMEMultipart()
    msg['Subject'] = 'Your Daily Sunrise Photo'
    msg['From'] = fromemail
    msg['To'] = toemail

    # Open the files in binary mode.  Let the MIMEImage class automatically
    # guess the specific image type.
    fp = open('upload-image.jpg', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'], frompass)
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()

while(1):
    now = datetime.datetime.now()

    if (now >= sunrise) and (did_upload == False):
        try:
            os.system(image_cmd)
            print("New sunrise image taken: " + str(now))
            send_email()
            print("Successfully emailed sunrise image to " + toemail)
            did_upload = True
        except Exception as e:
            print(e)

    if datetime.date.today() != current_date:
        current_date = datetime.date.today()
        print("Date changed: " + str(current_date))
        sunrise = city.sun(date=current_date, local=True)['sunrise'].replace(tzinfo=None)
        print("Today's sunrise: " + str(sunrise))
        did_upload = False  # reset the upload status for the new day
    
    time.sleep(1)
