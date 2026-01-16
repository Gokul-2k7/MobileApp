
from flask import request,render_template,redirect,url_for
from flaskapp import app
login={}

@app.route('/',methods=["GET","POST"])
def home():
    error=None
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        if name in login and login[name]==password:
            return f"HI {name}"
        else:
           error="Invalid username or password"        
    return render_template('index.html',error=error)
@app.route('/register',methods=["GET","POST"])
def register():
    Name=None
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        if name in login:
            error="Username exists"
            return render_template('register.html',error=error)
        login[name]=password
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/name=<name>/age=<age>')
def details(name,age):
    return f"{name} age is {age}"