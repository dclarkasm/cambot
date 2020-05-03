import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from getpass import getpass
from cryptography.fernet import Fernet
import json
from myexit import myexit

class Email:
    def __init__(self, creds_file):
        self.fromemail = None
        self.frompass = None
        self.toemail = None
        self.initialize(creds_file)

    def initialize(self, creds_file):
        if not os.path.exists(creds_file):
            self.fromemail = str(input("Please input outgoing email address (gmail only): "))
            self.frompass = str(getpass(prompt="Please input the password for the outgoing email account: "))
            toemail1 = str(input("Please input the incomming email address: "))
            toemail2 = str(input("Please input the incomming email address again: "))
            self.toemail = None
            
            if toemail1 == toemail2:
                self.toemail = toemail1
            else:
                print('The "To email" addresses do not match. Exiting.')
                myexit()

            # create secret key
            new_key = Fernet.generate_key()  # key length is 44 bytes

            # encrypt credentials
            f = Fernet(new_key)
            creds = {"fromemail":self.fromemail, "frompass":self.frompass, "toemail":self.toemail}
            encrypted_creds = f.encrypt(json.dumps(creds).encode())

            # save to creds_file
            with open (creds_file, 'wb') as cf:
                cf.write(new_key)
                cf.write(encrypted_creds)
        else:
            # grab credentials from creds_file
            encrypted_creds = None
            try:
                with open (creds_file, 'rb') as cf:
                    key = cf.read(44)   # they key is contained in the first 44 bytes
                    encrypted_creds = cf.read()
            except:
                print(e)
                print("Error reading credentials file. Exiting.")
                myexit()

            # decrypt credentials
            try:
                f = Fernet(key)
                creds = json.loads(f.decrypt(encrypted_creds).decode())
                self.fromemail = creds['fromemail']
                self.frompass = creds['frompass']
                self.toemail = creds['toemail']
            except Exception as e:
                print(e)
                print("Error reading credentials. Exiting.")
                myexit()

    def send_email(self, image_path):
        msg = MIMEMultipart()
        msg['Subject'] = 'Your Daily Birdhouse Photo'
        msg['From'] = self.fromemail
        msg['To'] = self.toemail

        # Open the files in binary mode.  Let the MIMEImage class automatically
        # guess the specific image type.
        fp = open(image_path, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(msg['From'], self.frompass)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
