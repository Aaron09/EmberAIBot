#this correctly sends an email

import smtplib

with open('emailTextFile') as file:     # allows the message to be composed of information from another file
    messageText = file.read()


server = smtplib.SMTP('smtp.gmail.com', 587) # only works for gmail service. Different host code will be needed for different email services
server.starttls()  # protects the username and password of the sender email
server.login("emberuiucbot@gmail.com", "emberbotproject123")# username and password of account that sends the email
                                                            # to enable an account to send an email, you must first go
                                                            # into the google security section of
                                                            # the account and enable "less-secure apps" or something similar to that name

msg = messageText # this can also be straight text
server.sendmail("emberuiucbot@gmail.com", "aaron.green281@gmail.com", msg)
server.quit()