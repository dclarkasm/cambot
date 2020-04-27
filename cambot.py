#!/usr/bin/env python3
import os
from datetime import datetime
import time
import yaml
import argparse
from email_wrapper import Email
from camera import Camera
from myexit import myexit

''' Todo:
 - Add LED PWM
 - Add method for shutdown override
 - Add emails for when errors occur
 - Add low battery indicator status to email
'''

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "path to YAML config file")
parser.add_argument("-c", "--creds_file", help = "path to credentials file")
args = parser.parse_args()

if args.file == None:
    print("--file is a required argument, Exiting")
    myexit(1)

if args.creds_file == None:
    print("--creds_file is a required argument, Exiting")
    myexit(1)

if __name__ == "__main__":
    trigger_time = None
    image_path = None
    with open(args.file) as f:
        data = yaml.load(f)
        trigger_time = tuple(data['trigger_time'])
        image_path = data['image_path']
    
    em = Email(args.creds_file)
    c = Camera(image_path)
    
    time_now = time.localtime()
    now = datetime.fromtimestamp(time.mktime(time_now))
    trigger_dt_w = list(time_now)
    trigger_dt_w[3] = trigger_time[0]
    trigger_dt_w[4] = trigger_time[1]
    trigger_dt_w[5] = trigger_time[2]
    trigger_dt = datetime.fromtimestamp(time.mktime(time.struct_time(tuple(trigger_dt_w))))
    if (now < trigger_dt):
        deltat = (trigger_dt - now).total_seconds()
        print("Sleeping for %d seconds..." % (deltat))
        time.sleep(deltat)   # sleep until it is time to take the image
    
    try:
        # take image here
        c.take_image()
        print("New birdhouse image taken: " + str(now))
        em.send_email(c.image_path)
        print("Successfully emailed birdhouse image to " + em.toemail)
    except Exception as e:
        print(e)
        myexit(1)
    finally:
        myexit(0)
    
