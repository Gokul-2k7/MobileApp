from flask import render_template,request,redirect,url_for,abort
from flaskapp import db
from flaskapp.posts.models import Post
from flaskapp.posts.forms import PostForm
from flask_login import current_user,login_required
from flask import Blueprint

posts=Blueprint('posts',__name__)
@posts.route('/new_posts',methods=['GET','POST'])
@login_required
def new_posts():
    form=PostForm()
    legend='New Post'
    if form.validate_on_submit():
        p=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('posts.html',form=form,legend=legend)

@posts.route('/home/<int:post_id>/update',methods=['GET','POST'])
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

@posts.route('/home/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    p = Post.query.get_or_404(post_id)
    if current_user!=p.author:
        abort(403)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('main.home'))

