# this correctly reads an email from a gmail account

import imaplib # this package is used to read emails from an account

msrvr = imaplib.IMAP4_SSL('imap.gmail.com',993) # creates the webserver that will be used to access the email
                                                # the host number varies depending on the email service used
                                                # this only works for gmail
username = 'emberuiucbot' # email account username which the emails will be read from
password = 'emberbotproject123' # email account password which the emails will be read from

msrvr.login(username, password) # logging the account into the webserver
stat,count = msrvr.select('Inbox') # selecting all of the emails in "Inbox"

stat, data = msrvr.fetch(count[0], '(UID BODY[TEXT])') # Not sure what this line does
print data[0][1] # Prints out the most recent email received; not familiar with more advanced mechanics
msrvr.close() # closing the server
msrvr.logout() # logging out of the server
