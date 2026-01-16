
from flask import request,render_template,redirect,url_for
from flaskapp import app
from flaskapp.models import db,User,Post

@app.route('/',methods=["GET","POST"])
def login():
    error=None
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        user = User.query.filter_by(username=name).first()
        if user and user.password == password:
            return redirect(url_for('home',name=name))
        else:
           error="Invalid username or password"        
    return render_template('index.html',error=error)
@app.route('/register',methods=["GET","POST"])
def register():
    error=None
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        user=User.query.filter_by(username=name).first()
        if user:
            error="Username exists"
            return render_template('register.html',error=error)
        user=User(username=name,email=f"{name}@gmail.com",password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home(name):
    return f"Hi {name}\nThis is the home page"