from imapidle import imaplib
import smtplib
import email

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('emberuiucbot@gmail.com', 'emberbotproject123')
mail.list()
mail.select('inbox')
isFirstEmail = True
completedOneEmail = False
mailReceived = False

senderEmail = ""
completeAddresses = []


for uid, msg in mail.idle():
    if not completedOneEmail:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('emberuiucbot@gmail.com', 'emberbotproject123')
        print "waiting for message"
        mail.select('inbox')
        typ, data = mail.search(None, 'ALL')
        ids = data[0]
        id_list = ids.split()
        # get the most recent email id
        latest_email_id = int( id_list[-1])

        typ, data = mail.fetch( latest_email_id, '(RFC822)' )

        if isFirstEmail:
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    varFrom = msg['from']
                    varTo = msg['to']

            # remove the brackets around the sender email address
            varFrom = varFrom.replace('<', '')
            varFrom = varFrom.replace('>', '')
            varTo = varTo.replace('>', '')
            varTo = varTo.replace('<', '')

            varFrom = varFrom.split()[-1]
            print "SENDER: "
            print varFrom
            senderEmail = varFrom
            incompleteAddresses = varTo.split()

            for possibleAddress in incompleteAddresses:
                if '@' in possibleAddress:
                    completeAddresses.append(possibleAddress)
            print "TO: "
            print completeAddresses

            isFirstEmail = False
            mail.logout()
            #mailReceived = True


#if mailReceived:
    server = smtplib.SMTP('smtp.gmail.com',
                          587)  # only works for gmail service. Different host code will be needed for different email services
    server.starttls()  # protects the username and password of the sender email
    server.login("emberuiucbot@gmail.com",
                 "emberbotproject123")  # username and password of account that sends the email
    # to enable an account to send an email, you must first go
    # into the google security section of
    # the account and enable "less-secure apps" or something similar to that name

    print "sending message to: " + senderEmail
    msg = "This was sent using an email bot"  # this can also be straight text
    server.sendmail("emberuiucbot@gmail.com", senderEmail, msg)
    print "message sent"
    server.quit()
    break


