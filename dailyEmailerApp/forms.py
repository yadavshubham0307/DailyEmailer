from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import PasswordField, EmailField, SubmitField, StringField, IntegerField,SelectField, TextAreaField, DateField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
import email_validator
import datetime
from .models import UserProfile, session
from .toxicityDetect import Messagefilter
from .smtpServer import SMTPServer


# Custom field for selecting day name
class DaySelectField(SelectField):
    def __init__(self, label='', **kwargs):
        super(DaySelectField, self).__init__(label, **kwargs)
        self.choices = [(i, datetime.date(1900, 1, i).strftime('%A')) for i in range(1, 8)]


# New User Registration Form 
class RegistrationForm(FlaskForm):
    
    # Validate the user email with DB
    def validate_email(self, email_to_check):
        # Filter the user details in DB
        with session.begin():
            user = session.query(UserProfile).filter_by(userName=email_to_check.data).first()
        session.close()
        # User already exist
        if user:
            raise ValidationError('Email already exist! Please Login or try another email.')
        
    
    firstName = StringField(label='First Name', validators=[DataRequired()])
    lastName = StringField(label = 'Last Name',validators=[DataRequired()])
    email = EmailField(label = 'Email', validators=[Email(), DataRequired()])
    password = PasswordField(label = "Password", validators=[DataRequired(), Length(min=8, message='Password should be at least %(min)d characters long')])
    rePassword = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo('password',message='Both password fields must be equal!')])
    gender = SelectField(label="Gender", choices=[('Male','Male'),('Female','Female'),('Other','Other')], validators=[DataRequired()])
    age = IntegerField(label='Age', validators=[DataRequired()])
    submit = SubmitField(label="Create Account")
    

# User Login Form
class LoginForm(FlaskForm):
    
    # Validate the user email with DB
    def validate_email(self, email_to_check):
        # Filter the user details in DB
        with session.begin():
            user = session.query(UserProfile).filter_by(userName=email_to_check.data).first()
        session.close()
        # User not exist
        if user == None:
            raise ValidationError('Email not exist! Please register.')
        

    email = EmailField(label="Email address", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField(label="Login")
    

# Add new Message Form
class AddMessageForm(FlaskForm):
    # Validate the message 
    def validate_message(self, message_to_check):
        #Check Message content is toxicity label
        messageFilter = Messagefilter()
        response = messageFilter.runFilter(message_to_check.data)
        
        if response != '': # If message content find toxic
            raise ValidationError(f'Message contains potentially harmful or offensive language like {response}')
        
    subject = StringField(label="Messgae Subject", validators=[DataRequired()])
    message = CKEditorField(label="Messgae" ,validators=[DataRequired()])
    recieverMail = EmailField(label="Reciever Email Address", validators=[DataRequired()])
    scheduleType = SelectField(label="Message Scheduled Type", choices=[('Daily','Daily'),('Once','Once'),('Weekly','Weekly'),('Monthly','Monthly'),('Yearly','Yearly')], validators=[DataRequired()])
    scheduleOn = StringField(label="Message Scheduled On")
    
    submit = SubmitField(label='Save')
    
    
#Add new mail server details form    
class AddHostForm(FlaskForm):
    
    smtp_host = StringField(label='SMTP Host', validators=[DataRequired()])
    smtp_port = IntegerField(label="SMTP Port", validators=[DataRequired()])
    username = EmailField(label='Username', validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    senderName = StringField(label='Sender Name', validators=[DataRequired()])
    senderMail = EmailField(label='Sender Mail', validators=[DataRequired()])
    submit = SubmitField(label='Save')
    
    
#  Contact Us form
class ContactUsForm(FlaskForm):
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name")
    email = EmailField(label="Email", validators=[DataRequired()])
    message = TextAreaField(label="What can help you with?", validators=[DataRequired()])
    submit  = SubmitField(label="Submit")
    
    
#Forgot Password Mail Input Form    
class ForgotMailVarificationForm(FlaskForm):
    # Validate the user email with DB
    def validate_email(self, email_to_check):
        # Filter the user details in DB
        with session.begin():
            user = session.query(UserProfile).filter_by(userName=email_to_check.data).first()
        session.close()
        # User not exist
        if not(user):
            raise ValidationError('Email not exist! Please try another email.')
    
    email = EmailField(label = 'Email', validators=[Email(), DataRequired()])
    submit = SubmitField(label="Submit")
    
#Password Change Form    
class PassordChangeForm(FlaskForm):
   
    password = PasswordField(label = "Password", validators=[DataRequired(), Length(min=8, message='Password should be at least %(min)d characters long')])
    rePassword = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo('password',message='Both password fields must be equal!')])
    submit = SubmitField(label="Change Password")