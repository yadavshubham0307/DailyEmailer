import smtplib
import ssl
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SMTPServer():
    def __init__(self,smtp_host, port, username, password):
        self.smtp_host = smtp_host
        self.port = port
        self.username = username
        self.password = password
        self.server = None
        self.connectionStatus = self.smtpConnection()
                
    #Establish the SMTP Mail connection
    def smtpConnection(self):
        try:
            # Connect to the SMTP server
            self.server = smtplib.SMTP(self.smtp_host, self.port)
            self.server.ehlo()
            # Start TLS encryption (if supported)
            self.server.starttls()
            # Login to the SMTP server
            self.server.login(self.username, self.password)
            
        except smtplib.SMTPAuthenticationError :
            raise Exception("Check your login credentials.")
        except smtplib.SMTPConnectError:
            raise Exception("Check the server address and port.")
        except smtplib.SMTPServerDisconnected:
            raise Exception("Try again later.")
        except socket.gaierror:
            raise Exception("Check the server address and port.")
        except smtplib.SMTPException as err:
            raise Exception(err)
        except Exception as err:
            raise Exception(err)
        
        
    #Close the SMTP Connection    
    def smtpClose(self):
        self.server.quit()
    
    #Sent mail    
    def sendmail(self,receiver_email,sender_mail, sender_name, subject, message ):
        # Create a MIMEText object for email content
        try:
            msg = MIMEMultipart()
            msg['From'] = f'{sender_name} <{sender_mail}>'
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'html'))
            self.server.sendmail(sender_mail, receiver_email, msg.as_string())
        except smtplib.SMTPHeloError:
            raise Exception("The Server refused the message.") 
        
    
        
