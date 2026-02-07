from flask import render_template,request,redirect,url_for,flash,Blueprint
from flaskapp import mail
from flaskapp.users.models import db,User
from flaskapp.posts.models import Post
from flaskapp.users.forms import Loginform, RegistrationForm,UpdateForm,RequestResetForm,ResetPasswordForm
from flaskapp import bcrypt
from flask_login import login_user,logout_user,login_required,current_user
from flaskapp.users.utils import save_picture,send_reset_email

users=Blueprint('users',__name__)
@users.route('/login',methods=["GET","POST"])
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
           error="Invalid password"        
    return render_template('index.html',error=error,form=form)

@users.route('/register',methods=["GET","POST"])
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
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form,error=error)


@users.route('/account')
@login_required
def account():
    if current_user.image_file:
        image_file=current_user.image_file
    else:
        image_file="default.jpg"
    image_file=url_for('static',filename='pics/'+ image_file)
    return render_template('account.html',user=current_user,image_file=image_file)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
@users.route('/account/update',methods=["GET","POST"])
@login_required
def update_account():
    form= UpdateForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file=form.image_file.data
            image=save_picture(image_file)
            current_user.image_file=image
        current_user.username=form.username.data
        current_user.email=form.email.data
        if form.password.data:
            current_user.password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    return render_template('update.html',form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=5,error_out=False,page=page)
    return render_template('user_posts.html',posts=posts,user=user)


@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    user=User.verify_token(token)
    if not user:
        flash('Invalid or expired token','failure')
        return redirect(url_for('users.request_reset'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_pass
        db.session.commit()
        flash('Your password has been updated!')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html',form=form)
        
@users.route('/request_reset',methods=['GET','POST'])
def request_reset():
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Link has sent to registered email,if exists','info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html',form=form)

