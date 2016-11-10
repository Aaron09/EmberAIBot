###########################
#   Ember Bot Project     #
#   UIUC CS 196 Fall 2016 #
#   Email Bot API Code    #
#   Author: Aaron Green   #
###########################

import EmailCleaner as Cleaner
import smtplib
import event_algorithm_v_1 as CalendarFinder
from email.mime.text import MIMEText

def getJob(jobs, chainID):
    return jobs[chainID][1]

def saveJob(jobs, chainID, recipients, jobType):
    jobs[chainID] = [recipients, jobType]
    print jobs
    return jobs

def executeJob(jobs, chainID, botUsername, botPassword, totalResponderDict):
    recipients, jobType = jobs[chainID][0], jobs[chainID][1]
    if jobType == "send_times":
        message = MIMEText(CalendarFinder.main(totalResponderDict[chainID]), "plain")
        server = startSendingServer(botUsername, botPassword)
        server.starttls()
        server.login(botUsername, botPassword)
        Cleaner.sendEmails(recipients, botUsername, message, server)
        terminateServer(server)

def startSendingServer(botUsername, botPassword):
    return smtplib.SMTP('smtp.gmail.com', 587)  # creates a gmail server through which to send emails

def terminateServer(server):
    server.quit()
