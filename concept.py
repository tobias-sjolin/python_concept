import sys
import imaplib
import getpass
import email
import email.header
import datetime

def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return
    
        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0], 'utf-8')
        fromEmail = email.utils.parseaddr(msg['From'])[1]
        print 'Message %s: %s' % (num, subject)
        print fromEmail
        print 'Raw Date:', msg['Date']
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")
        if fromEmail !="":
            import MySQLdb
            db = MySQLdb.connect(host="localhost", user=sys.argv[3], passwd=sys.argv[4],db="concept")

            cur = db.cursor()
            try:
                cur.execute("INSERT INTO tracker (email, subject) VALUES (%s, %s)", (fromEmail, subject))
                cur.commit()
            except MySQLdb.ProgrammingError, e:
                print 'There was a MySQL warning.  This is the info we have about it: %s' %(e)
            finally:
                cur.close()

M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    rv, data = M.login(sys.argv[1], sys.argv[2])
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    # ... exit or deal with failure...

print rv, data

rv, mailboxes = M.list()
if rv == 'OK':
    print "Mailboxes:"
    print mailboxes


rv, data = M.select("INBOX")
if rv == 'OK':
    print "Processing mailbox...\n"
    process_mailbox(M) # ... do something with emails, see below ...
    M.close()
M.logout()
