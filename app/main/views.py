from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required
from ..models import User,Post,Comment
from .forms import UpdateProfile
from ..requests import get_quotes
from .forms import PostForm,CommentForm,UpdatePostForm
from .. import db,photos
from flask_login import current_user

@main.route('/')
def index():
    
    post = Post.query.order_by(Post.time.desc()).all()
    hobbies = Post.query.filter_by(category = 'Hobbies').order_by(Post.time.desc()).all() 
    experiences = Post.query.filter_by(category = 'Experiences').order_by(Post.time.desc()).all()
    skills = Post.query.filter_by(category = 'Skills').order_by(Post.time.desc()).all()
    quotes = get_quotes()
    title ='Blog'
    return render_template('index.html', hobbies = hobbies, experiences = experiences, post = post, skills= skills, title=title,quotes = quotes)

  
  
    return render_template('index.html', hobbies = hobbies, experiences = experiences, post = post, skills= skills, title=title)

@main.route('/user/<uname>')
def profile(uname):

    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)  

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):

    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile',uname=uname))    


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
       
        db.session.add(user)
        db.session.commit()
       
        return redirect(url_for('.profile',uname=user.username))
    
    return render_template('profile/update.html',form =form)    

def save_image(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_main.root_path, 'static/photos', photo_name)
    photo.save(file_path)

    return photo_name

@main.route('/new_post', methods = ['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
       
        if form.post_pic_path.data:
            post_pic_path = form.post_pic_path.data     
           
            if form.validate_on_submit():

                new_post = Post(post=post,user_id=current_user._get_current_object().id,post_pic_path=post_pic_path,category=category,title=title)
                db.session.add(new_post)
                db.session.commit()
        
            return redirect(url_for('main.index'))
        else:
            post_pic_path = 'https://ciusss360.ca/wp-content/uploads/2018/03/Open.png'   
            if form.validate_on_submit():
                new_post = Post(post=post,user_id=current_user._get_current_object().id,post_pic_path=post_pic_path,category=category,title=title)
          
                db.session.add(new_post)
                db.session.commit()
            
            return redirect(url_for('main.index'))
   
    return render_template('post.html', form = form)

@main.route('/comment/<int:post_id>', methods = ['POST','GET'])
def comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    all_comments = Comment.query.filter_by(post_id = post_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        post_id = post_id
        new_comment = Comment(comment = comment,post_id = post_id)
     
        db.session.add(new_comment)
        db.session.commit()
     
        return redirect(url_for('.comment', post_id = post_id))
    return render_template('comment.html', form =form, post = post,all_comments=all_comments) 

@main.route('/index/<int:id>/delete',methods = ['GET','POST'])
@login_required
def delete(id):
    current_blog = Post.query.filter_by(id = id).first()

    if current_blog.user != current_user:
        abort(404)
    db.session.delete(current_blog)
    db.session.commit()

    return redirect(url_for('.index'))

@main.route('/update/<int:id>',methods = ['GET','POST'])
@login_required
def update_post(id):

    posts = Post.query.filter_by(id = id).first()
    if posts.user != current_user:
        abort(404)
    form = UpdatePostForm()
    if form.validate_on_submit():
        posts.title = form.title.data
        posts.post = form.post.data 
        posts.category = form.category.data
        posts.post_pic_path = form.post_pic_path.data

        db.session.add(posts)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('update_post.html',form = form)