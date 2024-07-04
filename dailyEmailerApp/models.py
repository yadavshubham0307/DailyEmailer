from sqlalchemy import Column, Integer, String,Boolean, ForeignKey, Date
from . import engine,Base,session
from sqlalchemy.orm import relationship
from . import bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    with session.begin():
        user = session.query(UserProfile).filter_by(userId = int(user_id)).first()
        #session.expunge_all()
        session.close()
    return user

# User Profile Model Class 
class UserProfile(Base, UserMixin):
    __tablename__ = 'user_profiles'
    
    userId = Column(Integer, primary_key=True)
    userName = Column(String, unique=True)
    firstName = Column(String(20))
    lastName = Column(String(20))
    password_hash = Column(String(20))
    gender = Column(String)
    verified = Column(Boolean, default=False)
    age = Column(Integer())
        
    #Establish One-To-Many relationship
    messages = relationship('Message', back_populates='user_profile')
    mail_servers = relationship('MailServer', back_populates='user_profile')
    message_logger = relationship('MessageLogger', back_populates='user_profile')
        

        
    @property
    def password(self):
        return self.password
       
    @password.setter    
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    def password_check(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def get_id(self):
        return self.userId

    def __repr__(self):
        return f"{self.userId}, {self.userName}, {self.firstName}, {self.lastName}, {self.password}, {self.gender}, {self.age}"
    


# All Messages Model Class    
class Message(Base):
    __tablename__ = "messages"
    
    messagesId = Column(Integer,primary_key=True)
    subject = Column(String)
    message = Column(String)
    scheduleType = Column(String, default='Once')
    scheduleOn = Column(String)
    receiverMail = Column(String)
    message_type = Column(String, default='Custom')
    message_status = Column(Boolean, default=False)
    user_id =Column(Integer, ForeignKey('user_profiles.userId'))
    
    
    #Establist bidirectional connection
    user_profile = relationship('UserProfile', back_populates='messages')
    
        
    def __repr__(self):
        return f"{self.messagesId}, {self.message}, {self.scheduleType}, {self.scheduleOn}, {self.receiverMail}"
        
        
        
#Mail Server Model Class
class MailServer(Base):
    __tablename__ = "mail_servers"
    
    serverId = Column(Integer, primary_key=True)
    host = Column(String)
    port = Column(Integer)
    loginId = Column(String)
    serverPassword = Column(String)
    senderMail = Column(String)
    senderName = Column(String)
    user_id =Column(Integer, ForeignKey('user_profiles.userId'))
    
    
    #Establist bidirectional connection
    user_profile = relationship('UserProfile', back_populates='mail_servers')

    
    def __repr__(self):
        return f"{self.serverId}, {self.port}, {self.loginId}, {self.serverPassword}, {self.senderMail}, {self.user_id}"
    

#Message Logger Model Class
class MessageLogger(Base):
    __tablename__ = "message_logger"
    
    id = Column(Integer, primary_key=True)
    messagesId = Column(Integer)
    message_status = Column(Boolean)
    message = Column(String)
    subject = Column(String)
    receiverMail = Column(String)
    messageOn = Column(Date)
    user_id =Column(Integer, ForeignKey('user_profiles.userId'))
    
    #Establist bidirectional connection
    user_profile = relationship('UserProfile', back_populates='message_logger')
    
    def __repr__(self):
        
        return f"{self.id}, {self.messageId}, {self.message_status}, {self.message}, {self.subject}, {self.receiverMail}, {self.messageOn}, {self.user_id}"
    




Base.metadata.create_all(engine)



    
    
    
    
    
    
    
    
    
    
    
    