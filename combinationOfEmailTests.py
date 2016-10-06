from imapidle import imaplib
import smtplib
import email
import EmailCleaner as Cleaner


senderEmail = ""
completeAddresses = []
botEmailUsername = "emberuiucbot@gmail.com"
botEmailPassword = "emberbotproject123"
# username and password of account that sends the email;
# to enable an account to send an email, you must first go
# into the google security section of
# the account and enable "less-secure apps" or something similar to that name


mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(botEmailUsername, botEmailPassword)
#mail.list()
mail.select('inbox')
mailReceived = False

for uid, msg in mail.idle():
  #  idleMail = imaplib.IMAP4_SSL('imap.gmail.com')
  #  idleMail.login(botEmailUsername, botEmailPassword)
    print "waiting for message"
  #  mail.select('inbox')
    typ, data = mail.search(None, 'ALL')
    ids = data[0]
    id_list = ids.split()
    # get the most recent email id
    latest_email_id = int( id_list[-1])

    typ, data = mail.fetch(latest_email_id, '(RFC822)')

    for response_part in data:
        print "boowop"
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1])
            varFrom = msg['from']
            varTo = msg['to']

            varFrom = Cleaner.cleanEmailString(varFrom)
            varTo = Cleaner.cleanEmailString(varTo)

            varFrom = varFrom.split()[-1]

            Cleaner.fromTest(varFrom)

            incompleteAddresses = Cleaner.setIncompleteEmailList(varTo, varFrom)
            completeAddresses = Cleaner.addEmailsToResponseList(incompleteAddresses)

            Cleaner.toTest(completeAddresses)

            mail.logout()
            mailReceived = True

    if mailReceived:
        server = imaplib.IMAP4_SSL('imap.gmail.com')
        print "yay"
        server.starttls()
        server.login(botEmailUsername, botEmailPassword)
        message = "This was sent using an email bot"  # this can be straight text or another String variable
        Cleaner.sendEmails(botEmailUsername, completeAddresses, message, server)
        mailReceived = False

        server.quit()


