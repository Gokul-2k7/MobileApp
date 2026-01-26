
from flask import request,render_template,redirect,url_for
from flaskapp import app
from flaskapp.models import db,User,Post
from flaskapp.forms import Loginform, RegistrationForm
from flaskapp import bcrypt
from flask_login import login_user,logout_user,login_required,current_user
@app.route('/login',methods=["GET","POST"])
def login():
    error=None
    form=Loginform()
    if form.validate_on_submit():
        name=form.username.data
        password=form.password.data
        user = User.query.filter_by(username=name).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user,form.remember_me.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
           error="Invalid password"        
    return render_template('index.html',error=error,form=form)

@app.route('/register',methods=["GET","POST"])
def register():
    error=None
    form=RegistrationForm()
    if form.validate_on_submit():
        name=form.username.data
        email=form.email.data
        password=form.password.data
        user=User.query.filter_by(username=name).first()
        if user:
            error="Username exists"
            return render_template('register.html',error=error,form=form)
        user=User(username=name,email=email,password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form,error=error)

@app.route('/')
def home():
    posts=Post.query.all()
    user=User()
    name=request.args.get("name")
    return render_template('home.html',posts=posts,current_user=current_user,user=user)

@app.route('/account')
@login_required
def account():
    return render_template('account.html',user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))