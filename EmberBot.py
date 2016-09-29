###########################
#   Ember Bot Project     #
#   UIUC CS 196 Fall 2016 #
#   Email Bot Code        #
#   Author: Aaron Green   #
###########################

from imapidle import imaplib
# imapidle is originally under MIT open source license, customized for specific project use;
# responsible for the idling of the mail server, waiting for incoming emails

import email
import EmailCleaner as Cleaner  # custom API made by Aaron Green for organizing EmberBot code
import smtplib   # used for sending the response email

botUsername = "emberuiucbot"
botPassword = "emberbotproject123"

# creates the server that will be responsivle for idling
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(botUsername, botPassword)
mail.select("Inbox")

uid = 0  # each email sent and received has an associated uid
receivedMail = False
usedUIDS = []  # to prevent an email in the idle box to be used twice

for resp in mail.idle():

    # resp contains an asterisk, uid, and "exists" message associated with each email
    for potentialUID in resp.split():   # looks for the uid
        if potentialUID.isdigit() and potentialUID not in usedUIDS:
            uid = potentialUID
            usedUIDS.append(uid)
            receivedMail = True

    if receivedMail:
        # a temporary mail server is created to fetch emails, since the original server must remain idling
        tempMailServer = imaplib.IMAP4_SSL("imap.gmail.com")
        tempMailServer.login(botUsername, botPassword)
        tempMailServer.select("Inbox")
        status, data = tempMailServer.fetch(uid, '(RFC822)')  # fetches the currently most recent email
        msg = email.message_from_string(data[0][1])  # pulls the message information from the email data

        # gathers the text from the "from" and "to" fields of the email
        varFrom = msg["From"]
        varTo = msg["To"]

        # removes brackets around email address / cleans it up
        varFrom = Cleaner.cleanEmailString(varFrom)
        varTo = Cleaner.cleanEmailString(varTo)

        # emails are fetched with their associated username as well, not just the email address
        # so we must remove all text other than email address
        varFrom = Cleaner.onlyGetAddress(varFrom.split())

        incompleteEmailList = Cleaner.setIncompleteEmailList(varTo, varFrom)
        completeEmailList = Cleaner.selectEmailAddresses(incompleteEmailList)

        # Tests to ensure the "from" and "to" fields are correctly parsed
        Cleaner.fromTest(varFrom)
        Cleaner.toTest(completeEmailList)
        # end tests

        receivedMail = False
        tempMailServer.close()  # closes the temporary server

        # the following code is responsible for sending the response emails

        server = smtplib.SMTP('smtp.gmail.com', 587)  # creates a gmail server through which to send emails
        server.starttls()  # protects username and password
        server.login(botUsername, botPassword)
        message = "This was sent using an email bot"  # this can be straight text or another String variable

        Cleaner.sendEmails(completeEmailList, botUsername, message, server)

        # when an email is sent, it is given a uid, so this must also be added to the used list
        # or the program will attempt to access it on the next loop, crashing the program because
        # necessary fields will be null
        usedUIDS.append(str(int(uid) + 1))

        server.quit()  # closes the temporary sending server
