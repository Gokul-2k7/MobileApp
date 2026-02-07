import os
class Config():
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SECRET_KEY='a1b2c3d4e5f6g7h8i9j0'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME= 'k.gokul27112007@gmail.com'
    MAIL_DEFAULT_SENDER= 'MAIL_USERNAME'
    MAIL_PASSWORD= "wlnggbotcirwarvp"