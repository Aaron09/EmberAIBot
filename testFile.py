import JobHandler as JobHandler
import EmailCleaner as Cleaner
import smtplib


with open("BotCredentials") as file:
    botUsername = file.readline().strip()
    botPassword = file.readline().strip()

server = JobHandler.startSendingServer(botUsername, botPassword)
server.starttls()
server.login(botUsername, botPassword)
Cleaner.sendEmails(["aaron.green281@gmail.com"], botUsername, "Hello World", server)
JobHandler.terminateServer(server)
