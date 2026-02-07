from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail




mail=Mail()
db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager = LoginManager()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class='flaskapp.config.Config'):
    app=Flask(__name__)
    app.config.from_object(config_class)
    from flaskapp.users.routes import users
    from flaskapp.posts.routes import posts
    from flaskapp.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    return app