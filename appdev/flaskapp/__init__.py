
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
app.config['SECRET_KEY']='a1b2c3d4e5f6g7h8i9j0'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
from appdev.flaskapp import routes,models
