###########################
#   Ember Bot Project     #
#   UIUC CS 196 Fall 2016 #
#   Email Bot API Code    #
#   Author: Aaron Green   #
###########################

import api_calls as CalendarAPI
from imapidle import imaplib
import email
import EmailCleaner as Cleaner

def hasNotSignedUpTag(subjectLine):
    if "Not all users signed up for Ember" in subjectLine:
        return True
    else:
        return False

def organizeUnverifiedForBody(addresses):
    bodyPart = ""
    for i in range(0, len(addresses)):
        if i == len(addresses) - 1:
            bodyPart += addresses[i]
        else:
            bodyPart += addresses[i] + " and "
    return bodyPart + " "

def grabUnverified(unverifiedDict, addresses, chainID):
    unverifiedDict[chainID] = []
    for address in addresses:
        if not CalendarAPI.credientials_exist(address):
            unverifiedDict[chainID].append(address)
    return unverifiedDict

def parseEmailForAll(uid):
    with open("BotCredentials") as file:
        botUsername = file.readline().strip()
        botPassword = file.readline().strip()

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
    time = parseDateForTime(msg["Date"])
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

    tempMailServer.close()  # closes the temporary server

    return (completeEmailList, varFrom, varTo, body, time, subjectKey)

def checkAllForVerification(addresses):
    for address in addresses:
        if not CalendarAPI.credientials_exist(address):
            return False
    return True

def readResponseForTimes(response):
    if type(response) is not str:
        message = response[0].as_string(unixfrom=True)
        message = str(message)
        pastUTF8 = False
        trueResponse = ""
        for i in range(0,len(message)):
            if message[i-1] == "-" and message[i] == "8":
                pastUTF8 = True
            elif message[i] == "O" and message[i+1] == "n":
                pastUTF8 = False
                break
            elif pastUTF8:
                trueResponse += message[i]
    else:
        trueResponse = response
    trueResponse = trueResponse.strip()
    responseDict = {}
    for potentialDigit in trueResponse:
        if potentialDigit == ">":
            break
        elif potentialDigit.isdigit():
            if potentialDigit in responseDict:
                responseDict[int(potentialDigit)] += 1
            else:
                responseDict[int(potentialDigit)] = 1
    return responseDict

def readResponseForTimesForExistingDict(responseDict, response):
    if type(response) is not str:
        message = response[0].as_string(unixfrom=True)
        message = str(message)
        pastUTF8 = False
        trueResponse = ""
        for i in range(0,len(message)):
            if message[i-1] == "-" and message[i] == "8":
                pastUTF8 = True
            elif message[i] == "O" and message[i+1] == "n":
                pastUTF8 = False
                break
            elif pastUTF8:
                trueResponse += message[i]
    else:
        trueResponse = response
    trueResponse = trueResponse.strip()
    for potentialDigit in trueResponse:
        if potentialDigit == ">":
            break
        elif potentialDigit.isdigit():
            if int(potentialDigit) in responseDict:
                responseDict[int(potentialDigit)] += 1
            else:
                responseDict[int(potentialDigit)] = 1
    return responseDict

def parseDateForTime(date):
    timeKey = ""
    for potentialDigit in date:
        if potentialDigit.isdigit():
            timeKey += potentialDigit
    return timeKey

def findIdInSubjectLine(subjectLine):
    pastDash = False
    dashOccurances = 0
    id = ""
    for letter in subjectLine:
        if letter == "-":
            dashOccurances += 1
        elif dashOccurances == 2:
            pastDash = True
        if pastDash:
            id += letter
    return id
