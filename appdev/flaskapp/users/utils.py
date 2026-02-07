
from flaskapp import mail
from flask import current_app
from flask_mail import Message
import secrets
import os
from PIL import Image
from flask import url_for
def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,ext= os.path.splitext(form_picture.filename)
    picture_fn=random_hex+ext
    picture_path=os.path.join(current_app.root_path,'static/pics',picture_fn)
    img = Image.open(form_picture)
    img.thumbnail((200,200))
    img.save(picture_path)
    return picture_fn

def send_reset_email(user):
    print("MAIL_USERNAME =", current_app.config.get('MAIL_USERNAME'))
    print("MAIL_DEFAULT_SENDER =", current_app.config.get('MAIL_DEFAULT_SENDER'))
    print("MAIL OBJECT =", mail)
    token=user.get_reset_token()
    msg=Message('Password Reset Request',recipients=[user.email])
    msg.body=f'''To reset your password, visit the following link:
{url_for('users.reset_token',token=token,_external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
