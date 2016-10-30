###########################
#   Ember Bot Project     #
#   UIUC CS 196 Fall 2016 #
#   Email Bot API Code    #
#   Author: Aaron Green   #
###########################

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
