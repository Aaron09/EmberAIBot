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
import JobHandler

storageDict = {}
hasRespondedDict = {}
totalResponderDict = {}
timeFrequencyDict = {}
jobDict = {} # holds the unprocessable jobs because of verification
usersNotSignedUpDict = {}

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
chainIDList = []
invalidUserMessage = "please go to the Ember website and sign up!\nOnce you've done this, reply to this email letting me know you've signed up!"

for resp in mail.idle():

    # takes in respList, needs to return uid, usedUIDS, receivedMail
    respList = resp.split()
    uid, usedUIDS, receivedMail = Cleaner.parseRespList(respList, usedUIDS)
    # resp contains an asterisk, uid, and "exists" message associated with each email

    if receivedMail:

        # Can the input processing be broken into another file?

        properToField = True
        # takes in uid
        # need to return completeEmailList, varFrom, varTo, time, body, subjectKey
        completeEmailList, varFrom, varTo, body, time, subjectKey = Parser.parseEmailForAll(uid)
        receivedMail = False

        # generates unique id for each email chain
        chainID = Parser.findIdInSubjectLine(subjectKey)
        if chainID in storageDict:
            isFirstInChain = False
        else:
            chainID = Cleaner.identifier(subjectKey, varFrom, time)
            isFirstInChain = True

        # each time an email is received that is part of an existing chain, we
        # check if that job can be processed
        # this doesn't work. But it shows the theory behind it. I need a way
        # to know when someone know signs up for the service, then I can check
        # if they are a part of a job I am waiting to complete, if so, I check if
        # I can complete that job.

        # Ophir is making the way to tell me if someone new signs up for the service
        # So I need a way to wait and call the method when someone knew signs up
        # Could I have an eternally running "while(True)" that checks every so often
        # if someone knew has signed up, and if so, how do I then complete the rest
        # of what needs to be done.

        if chainID in jobDict:
            if Parser.checkAllForVerification(totalResponderDict[chainID]):
                jobType = JobHandler.getJob(jobDict, chainID)
                JobHandler.executeJob(jobDict, chainID, botUsername, botPassword, totalResponderDict)

        # if the email is sent directly to the bot (via the "TO" field),
        # the bot will not respond
        if isFirstInChain:
            for potentialEmail in varTo.split():
                if botUsername in potentialEmail:
                    properToField = False

        # Response handling code is too complicated and long in this file.
        # I need to break it into another file or something alone those lines.

        # if the bot is not in the "TO" field
        if properToField:
            if chainID in storageDict and isFirstResponse:
                isFirstInChain = False
                isFirstResponse = False
                # begins the list of who has responded
                hasRespondedDict[chainID] = [varFrom]
                hasRespondedDict[chainID].sort()
                print hasRespondedDict[chainID]
                # total list of people who need to respond
                print totalResponderDict[chainID]

                # gathers the preferred times of the responder
                timeFrequencyDict[chainID] = Parser.readResponseForTimes(body)

                # if everyone has responded, this triggers if the person is setting
                # up an event with themself
                if hasRespondedDict[chainID] == totalResponderDict[chainID]:
                    print "all responses completed"
                    print timeFrequencyDict[chainID]
                    timeDecidedResponse = True
            elif chainID in storageDict:
                # must convert each response address to list to append to
                # current list in id
                if not varFrom in hasRespondedDict:
                    tempResponseList = hasRespondedDict[chainID]
                    tempResponseList.append(varFrom)
                    hasRespondedDict[chainID] = tempResponseList
                    # sort each time for comparison to total list
                    hasRespondedDict[chainID].sort()
                    print hasRespondedDict[chainID]
                    print totalResponderDict[chainID]

                    # gathers the preferred times of the responder
                    timeFrequencyDict[chainID] = Parser.readResponseForTimesForExistingDict(timeFrequencyDict[chainID], body)

                    if hasRespondedDict[chainID] == totalResponderDict[chainID]:
                        print "all responses completed"
                        print timeFrequencyDict[chainID]
                        timeDecidedResponse = True
            else:
                # this is the email that begins the chain
                isFirstInChain = True
                # set everyone that needs to respond
                totalResponderDict[chainID] = completeEmailList
                storageDict[chainID] = varFrom
                totalResponderDict[chainID].sort()
                print totalResponderDict[chainID]


            # Can the output processing be broken into another file?

            # the following code is responsible for sending the response emails
            if isFirstInChain or timeDecidedResponse:
                # creates a gmail server through which to send emails
                server = JobHandler.startSendingServer(botUsername, botPassword)
                server.starttls()
                server.login(botUsername, botPassword)

                executable = True

                if isFirstInChain:
                    if Parser.checkAllForVerification(completeEmailList):
                        print "All Validated"
                        msg = MIMEText(CalendarFinder.main(completeEmailList), "plain")
                        msg['Subject'] = "Times to meet --" + chainID
                        isFirstInChain = False
                    else:
                        print "Not all addresses validated. Job being saved."
                        invalidUsers = Parser.grabUnverified(usersNotSignedUpDict, completeEmailList, chainID)
                        jobDict = JobHandler.saveJob(jobDict, chainID, completeEmailList, "send_times")
                        msg = MIMEText(Parser.organizeUnverifiedForBody(invalidUsers[chainID]) + invalidUserMessage, "plain")
                        msg["subject"] = "Not all users signed up for Ember --" + chainID
                        Cleaner.sendEmails(invalidUsers[chainID], botUsername, msg, server)
                        executable = False
                        isFirstInChain = False
                else:
                    msg = MIMEText(CalendarFinder.find_best_time_and_email(timeFrequencyDict[chainID], totalResponderDict[chainID]))
                    msg['Subject'] = "This is your decided time! --" + chainID
                    timeDecidedResponse = False

                if executable:
                    msg['From'] = botUsername
                    Cleaner.sendEmails(completeEmailList, botUsername, msg, server)

                JobHandler.terminateServer(server) # closes the temporary sending server
