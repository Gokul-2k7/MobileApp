from flaskapp import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired, Email, Length
from flaskapp.models import User
from wtforms import ValidationError


class Loginform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Password',validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Submit')
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('User not found. Please register first.')
    

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Sign Up')
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')
    def validate_confirm_password(self,confirm_password):
        if confirm_password.data != self.password.data:
            raise ValidationError('Passwords do not match. Please try again.')