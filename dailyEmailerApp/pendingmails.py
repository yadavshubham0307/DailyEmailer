from .models import UserProfile, Message, MailServer, session
from .maildate import DateFinder


# Find User's pendings message List
def pending_messages(userId):
    messeges = []
    with session.begin():
        messeges = session.query(Message).filter(Message.user_id == userId).filter(Message.message_status == True).all()
        session.close()
    
    for message in messeges:
        msg_pemding_date = DateFinder(message.scheduleOn, message.scheduleType,'pending')
        message.scheduleOn = msg_pemding_date
    return messeges