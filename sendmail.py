#!/usr/bin/python3
import smtplib
import argparse
import os

defFrom = os.getenv("DEFAULT_FROM")

def prompt(prompt):
    return input(prompt).strip()

def sendmail_fct(arg):
    with open(args.infile.name) as f:
        data = f.read()
    sendMail(args.mailFrom, args.rcpt, args.subject, data)

def prompt_fct():
    trennzeichen = " "
    fromaddr = prompt("From: ")
    toaddrs = prompt("To: ").split()
    subject = prompt("Subject: ").split()
    print("Enter message, end with ^D (Unix) or ^Z (Windows):")
    # Add the From: and To: headers at
    # the start!
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (fromaddr, ", % ".join(toaddrs),  ", % ".join(subject)))

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        msg = msg + line

    subject = trennzeichen.join(subject)
    sendMail(fromaddr, toaddrs, subject, msg)

def sendMail(fromaddr, toaddrs, subject, msg):
    msg = "Subject: "+subject+"\r\n\r\n"+msg
    print("Message length is", len(msg))
    server = smtplib.SMTP('localhost',25)
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    if server.quit():
        exit()

if not len(argv) > 1:
    prompt_fct()

parser = argparse.ArgumentParser(description="sendmail", exit_on_error=False)
parser.add_argument("rcpt", type=None, help="recipient of the email")
parser.add_argument("--mailFrom", "-f", type=None, required=False, default=defFrom, help="sender of the email")
parser.add_argument("--subject", "-s", type=None, default="---", help="subject of the email")
parser.parse_args(['-'])
parser.add_argument('infile', type=argparse.FileType('r'), default=argparse.SUPPRESS)
parser.set_defaults(func=sendmail_fct)

args = parser.parse_args()
try:
    args.func(args)
except AttributeError:
    parser.print_help()
    parser.exit()
    prompt_fct()
