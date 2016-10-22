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
from email.mime.text import MIMEText
import event_algorithm_v_1 as CalendarFinder
import EmailParser as Parser

storageDict = {}
hasRespondedDict = {}
totalResponderDict = {}
timeFrequencyDict = {}

# to hide the username and password on github
with open("BotCredentials") as file:
    botUsername = file.readline().strip()
    botPassword = file.readline().strip()

# creates the server that will be responsible for idling
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(botUsername, botPassword)
mail.select("Inbox")

uid = 0  # each email sent and received has an associated uid
receivedMail = False
usedUIDS = []  # to prevent an email in the idle box to be used twice
isFirstInChain = False
isFirstResponse = True
timeDecidedResponse = False

for resp in mail.idle():

    # resp contains an asterisk, uid, and "exists" message associated with each email
    respList = resp.split()
    for i in range(0, len(respList)):   # looks for the uid
        potentialUID = respList[i]
        if potentialUID.isdigit() and potentialUID not in usedUIDS and respList[i+1] == "EXISTS":
            uid = potentialUID
            usedUIDS.append(str(uid))
            receivedMail = True

    if receivedMail:
        properToField = True

        # a temporary mail server is created to fetch emails, since the original server must remain idling
        tempMailServer = imaplib.IMAP4_SSL("imap.gmail.com")
        tempMailServer.login(botUsername, botPassword)
        tempMailServer.select("Inbox")
        status, data = tempMailServer.fetch(uid, '(RFC822)')  # fetches the currently most recent email
        msg = email.message_from_string(data[0][1])  # pulls the message information from the email data

        # gathers the text from the "from" and "to" fields of the email
        varFrom = msg["From"]
        varTo = msg["To"]
        subjectKey = msg["Subject"]
        time = Parser.parseDateForTime(msg["Date"])
        body = msg.get_payload()

        # removes brackets around email address / cleans it up
        varFrom = Cleaner.cleanEmailString(varFrom)
        varTo = Cleaner.cleanEmailString(varTo)

        # emails are fetched with their associated username as well, not just the email address
        # so we must remove all text other than email address
        varFrom = Cleaner.onlyGetAddress(varFrom.split())

        incompleteEmailList = Cleaner.setIncompleteEmailList(varTo, varFrom)
        incompleteEmailList = Cleaner.removeRedundantAddresses(incompleteEmailList)
        completeEmailList = Cleaner.selectEmailAddresses(incompleteEmailList)

        # Tests to ensure the "from" and "to" fields are correctly parsed
        Cleaner.fromTest(varFrom)
        Cleaner.toTest(completeEmailList)
        # end tests

        # generates unique id for email chain
        chainID = Cleaner.identifier(subjectKey, varFrom, time)

        receivedMail = False
        tempMailServer.close()  # closes the temporary server

        # function to detect email chain id in received email
        id = Parser.findIdInSubjectLine(subjectKey)

        # if the email is sent directly to the bot (via the "TO" field),
        # the bot will not respond
        if isFirstInChain:
            for potentialEmail in varTo.split():
                if botUsername in potentialEmail:
                    properToField = False

        # if the bot is not in the "TO" field
        if properToField:
            if id in storageDict and isFirstResponse:
                isFirstInChain = False
                isFirstResponse = False
                # begins the list of who has responded
                hasRespondedDict[id] = [varFrom]
                hasRespondedDict[id].sort()
                print hasRespondedDict[id]
                # total list of people who need to respond
                totalResponderDict[id].sort()
                print totalResponderDict[id]

                # gathers the preferred times of the responder
                timeFrequencyDict[id] = Parser.readResponseForTimes(body)

                # if everyone has responded
                if hasRespondedDict[id] == totalResponderDict[id]:
                    print "all responses completed"
                    print timeFrequencyDict[id]
                    timeDecidedResponse = True
            elif id in storageDict:
                # must convert each response address to list to append to
                # current list in id
                tempRespList = hasRespondedDict[id]
                tempRespList.append(varFrom)
                hasRespondedDict[id] = tempRespList
                # sort each time for comparison to total list
                hasRespondedDict[id].sort()
                print hasRespondedDict[id]
                totalResponderDict[id].sort()
                print totalResponderDict[id]

                # gathers the preferred times of the responder
                timeFrequencyDict[id] = Parser.readResponseForTimesForExistingDict(timeFrequencyDict[id], body)

                if hasRespondedDict[id] == totalResponderDict[id]:
                    print "all responses completed"
                    print timeFrequencyDict[id]
                    timeDecidedResponse = True
            else:
                # this is the email that begins the chain
                isFirstInChain = True
                # set everyone that needs to respond
                totalResponderDict[chainID] = completeEmailList
                storageDict[chainID] = varFrom
                totalResponderDict[chainID].sort()
                print totalResponderDict[chainID]

            # the following code is responsible for sending the response emails
            if isFirstInChain or timeDecidedResponse:
                server = smtplib.SMTP('smtp.gmail.com', 587)  # creates a gmail server through which to send emails
                server.starttls()  # protects username and password
                server.login(botUsername, botPassword)
                
                if isFirstInChain:
                    msg = MIMEText(CalendarFinder.main(completeEmailList), "plain")
                else:
                    msg = MIMEText(CalendarFinder.find_best_time_and_email(timeFrequencyDict[id]))
                if timeDecidedResponse:
                    msg['Subject'] = "This is your decided time! --" + chainID
                    recipients = totalResponderDict[id]
                else:
                    msg['Subject'] = "Times to meet --" + chainID
                    recipients = completeEmailList

                msg['From'] = botUsername

                Cleaner.sendEmails(recipients, botUsername, msg, server)

                if timeDecidedResponse:
                    timeDecidedResponse = False
                else:
                    isFirstInChain = False

                server.quit()  # closes the temporary sending server
