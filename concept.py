import sys
import imaplib
import getpass
import email
import datetime

M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    M.login(sys.argv[1], sys.argv[2])
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    # ... exit or deal with failure...

rv, mailboxes = M.list()
if rv == 'OK':
    print "Mailboxes:"
    print mailboxes

rv, data = M.select("Top Secret/PRISM Documents")
if rv == 'OK':
    print "Processing mailbox...\n"
    process_mailbox(M) # ... do something with emails, see below ...
    M.close()
M.logout()
