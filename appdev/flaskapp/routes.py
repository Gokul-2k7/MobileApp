
from flask import abort, request,render_template,redirect,url_for
from flaskapp import app
from flaskapp.models import db,User,Post
from flaskapp.forms import Loginform, RegistrationForm,UpdateForm,PostForm
from flaskapp import bcrypt
from flask_login import login_user,logout_user,login_required,current_user
import secrets
import os
from PIL import Image 

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
    return render_template('home.html',posts=posts,current_user=current_user)

@app.route('/account')
@login_required
def account():
    if current_user.image_file:
        image_file=current_user.image_file
    else:
        image_file="default.jpg"
    image_file=url_for('static',filename='pics/'+ image_file)
    return render_template('account.html',user=current_user,image_file=image_file)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/new_posts',methods=['GET','POST'])
@login_required
def new_posts():
    form=PostForm()
    legend='New Post'
    if form.validate_on_submit():
        p=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('posts.html',form=form,legend=legend)

@app.route('/home/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    legend="Update Post"
    form=PostForm()
    p=Post.query.filter_by(id=post_id).first()
    if form.validate_on_submit():
        p.title=form.title.data
        p.content=form.content.data
        db.session.commit()
    elif request.method=='GET':
        form.title.data=p.title
        form.content.data=p.content
    return render_template('posts.html',form=form,legend=legend)

@app.route('/home/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    p = Post.query.get_or_404(post_id)
    if current_user!=p.author:
        abort(403)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('home'))


    
@app.route('/account/update',methods=["GET","POST"])
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
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    return render_template('update.html',form=form)

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,ext= os.path.splitext(form_picture.filename)
    picture_fn=random_hex+ext
    picture_path=os.path.join(app.root_path,'static/pics',picture_fn)
    img = Image.open(form_picture)
    img.thumbnail((200,200))
    img.save(picture_path)
    return picture_fn