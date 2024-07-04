from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer




app = Flask(__name__)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)

#Configur the SECRET KEY
app.config['SECRET_KEY'] = ''
#Configur the REMEMBER COOKIE DURATION
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30) 

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
engine = create_engine('sqlite:///dailyemailer.db',echo=True)
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()
login_manager = LoginManager(app)


from dailyEmailerApp import models

from dailyEmailerApp import routes







