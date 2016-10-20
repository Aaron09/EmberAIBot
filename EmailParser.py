###########################
#   Ember Bot Project     #
#   UIUC CS 196 Fall 2016 #
#   Email Bot API Code    #
#   Author: Aaron Green   #
###########################

def readResponseForTimes(response):
    responseDict = {}
    for potentialDigit in response:
        if potentialDigit == ">":
            break
        elif potentialDigit.isdigit():
            if potentialDigit in responseDict:
                responseDict[potentialDigit] += 1
            else:
                responseDict[potentialDigit] = 1
    return responseDict

def readResponseForTimesForExistingDict(responseDict, response):
    for potentialDigit in response:
        if potentialDigit == ">":
            break
        elif potentialDigit.isdigit():
            if potentialDigit in responseDict:
                responseDict[potentialDigit] += 1
            else:
                responseDict[potentialDigit] = 1
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
