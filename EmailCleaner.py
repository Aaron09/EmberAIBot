###########################
#   Ember Bot Project     #
#   UIUC CS 196 Fall 2016 #
#   Email Bot API Code    #
#   Author: Aaron Green   #
###########################

def parseRespList(respList, usedUIDS):
    # resp contains an asterisk, uid, and "exists" message associated with each email
    uid = 0
    receivedMail = False
    for i in range(0, len(respList)):   # looks for the uid
        potentialUID = respList[i]
        if potentialUID.isdigit() and potentialUID not in usedUIDS and respList[i+1] == "EXISTS":
            uid = potentialUID
            usedUIDS.append(str(uid))
            receivedMail = True
    return (uid, usedUIDS, receivedMail)


def cleanEmailString(emailAddress):
    emailAddress = emailAddress.replace('<', '')
    emailAddress = emailAddress.replace('>', '')
    emailAddress = emailAddress.replace('"', '')
    emailAddress = emailAddress.replace(',', '')
    return emailAddress

def selectEmailAddresses(listOfPossibleAddresses):
    addresses = []
    for potentialAddress in listOfPossibleAddresses:
        if '@' in potentialAddress:
            addresses.append(potentialAddress)
    return addresses

def sendEmails(listOfEmails, senderEmail, msg, sendServer):
    for address in listOfEmails:
        print "sending message to: " + address
        if type(msg) is not str:
            msg = msg.as_string()
        sendServer.sendmail(senderEmail, address, msg)
        print "message sent"

def onlyGetAddress(potentialEmailList):
    email = ""
    for potentialEmail in potentialEmailList:
        if "@" in potentialEmail:
            email = potentialEmail
    return email

def setIncompleteEmailList(toField, fromField):
    uncleanedAddresses = toField.split()
    uncleanedAddresses.append(fromField)
    return uncleanedAddresses

def removeRedundantAddresses(emailList):
    emails = []
    for email in emailList:
        if email not in emails:
            emails.append(email)
    return emails

def toTest(completeAddressList):
    print "TO: "
    print completeAddressList

def fromTest(testSenderEmail):
    print "SENDER: "
    print testSenderEmail

def identifier(subject, address, time):
    subjectSect = subject[len(subject)-4:len(subject)]
    addressSect = address[0:4]
    id = subjectSect + addressSect + time
    return id
