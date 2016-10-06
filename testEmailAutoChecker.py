# this file will test auto-checking for receiving of emails on the bot account

# this correctly waits for an email to be received, and then prints "EXISTS" when it receives an email
from imapidle import imaplib

m = imaplib.IMAP4_SSL('imap.gmail.com')
m.login('emberuiucbot', 'emberbotproject123')
m.select()

for uid, msg in m.idle():
    print msg



