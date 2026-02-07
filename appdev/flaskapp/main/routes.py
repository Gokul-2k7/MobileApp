from flask import render_template,request,Blueprint
from flaskapp.posts.models import Post
from flask_login import current_user

main=Blueprint('main',__name__)
@main.route('/')
def home():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,error_out=False,page=page)
    return render_template('home.html',posts=posts,current_user=current_user)
