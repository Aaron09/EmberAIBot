###########################
#   Ember Bot Project     #
#   UIUC CS 196 Fall 2016 #
#   Email Bot API Code    #
#   Author: Aaron Green   #
###########################

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
        sendServer.sendmail(senderEmail, address, msg.as_string())
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

def identifier(subject, address):
    subjectSect = subject[len(subject)-4:len(subject)]
    addressSect = address[0:4]
    id = subjectSect + addressSect
    return id
