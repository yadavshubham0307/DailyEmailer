''''
This script is work as a cron job and run daily as scheduled time 
DailyRunner Class Read the all active messages and find today scheduled message list using DataFinder Module
Sent the today's Scheduled Mail and save the message log on DB
'''


import os
import sys

# Replace below activated_this.py path with your path
activate_this = '/home/dailyemailer/automail/venv/bin/activate_this.py'  

with open(activate_this) as f:
    exec(f.read(),dict(__file__=activate_this))


#Replace below venv main path with your path
virtualenv_path = '/home/dailyemailer/automail'
sys.path.append(virtualenv_path)


from dailyEmailerApp import session
from dailyEmailerApp.models import Message, MailServer, UserProfile, MessageLogger
from dailyEmailerApp.maildate import DateFinder
from dailyEmailerApp.smtpServer import SMTPServer
from datetime import datetime



class DailyRunner:
    # Run Cron job
    def run(self):
        
        # User List
        users = self.usersFinder()
    
        # Iterate on Users
        for user in users:
            #User Mail Server Details
            mailserver = self.MailServer(user.userId, user.firstName) 
            #User Activated Message List
            actiavted_messages =  self.Messages(user.userId)
            
            #Iterate on activated messages
            for message in actiavted_messages:
                date_format = "%Y-%m-%d"
                #Find Today's scheduled message date
                messageDateFind = DateFinder(message.scheduleOn, message.scheduleType,'current')
                if str(messageDateFind) == '':
                    continue
                #Convert in message string date in date type
                messageDate = datetime.strptime(str(messageDateFind),date_format).date()

                try:
                    #Connect with SMTP Server
                    smtpServer = SMTPServer(mailserver.host, mailserver.port, mailserver.loginId, mailserver.serverPassword)
                    
                    #Sent user's Message
                    smtpServer.sendmail(message.receiverMail, mailserver.senderMail, user.firstName, message.subject, message.message)
                    
                    #Save the message Sent Log
                    messageLog = MessageLogger(messagesId = message.messagesId, message_status = True, message = message.message, subject = message.subject, receiverMail = message.receiverMail, messageOn = messageDate, user_id = user.userId)
                    session.add(messageLog)
                    
                    #Close the connections
                    smtpServer.smtpClose()
                    session.commit()
                    
                    #If user's message Scheduled type Once than convert the active status into unactive
                    if message.scheduleType == 'Once':
                        message.message_status = False
                        session.add(message)
                        session.commit()
                        
                except Exception as e: 
                    #if any Exception occur during Sent user mail than log the message Failed  
                    messageLog = MessageLogger(messagesId = message.messagesId, message_status = False, message = message.message, subject = message.subject, receiverMail = message.receiverMail, messageOn = messageDate, user_id = user.userId)
                    session.add(messageLog)
                    session.commit()
                    if message.scheduleType == 'Once':
                        message.message_status = False
                        session.add(message)
                        session.commit()




    #All user list find from DB
    def usersFinder(self):
        users = session.query(UserProfile).all()
        return users

    #Find user mail server details custom or default
    def MailServer(self,userID,userName):
        mailserver = session.query(MailServer).filter_by(user_id = userID).first()
        if mailserver :
            return mailserver
        else:
            serverPassword = ''   #Write your mail server passsword
            senderMail = ''       #Write our mail address
            loginID = ''          #Write your mail username
            port = ''             #Write your mail port
            host = ''             #Write your mail host
            
            default_mailserver = MailServer(serverId = 0, host=host, port=port, loginId=loginID, serverPassword=serverPassword,senderName= userName, senderMail = senderMail, user_id = 0)
            return default_mailserver

    #Find all activaed Messages for particualr userId
    def Messages(self,userId):
        msg = session.query(Message).filter_by(message_status = True).filter_by(user_id = userId)
        return msg






if __name__ == "__main__":
    cronjob = DailyRunner()
    cronjob.run()



