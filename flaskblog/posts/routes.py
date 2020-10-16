import os
import secrets
from flask import flash, redirect, render_template, url_for, abort, request, current_app
from flaskblog import db, app, photos
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import PostForm, CommentForm
from flask_login import current_user, login_required


@app.route('/post/new',  methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit() and 'image_1' in request.files and 'image_2' in request.files:
        image_1 = photos.save(request.files.get(
            'image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get(
            'image_2'), name=secrets.token_hex(10) + ".")

        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user, image_1=image_1, image_2=image_2)
        db.session.add(post)
        db.session.commit()
        flash('Your post was just added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_post.html', title='Add Post', form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    if form.validate_on_submit():
        comment = Comment(name=form.username.data,
                          content=form.content.data, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment was added!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('portfolio.html', post=post, title=post.title, form=form, comments=comments)


@app.route('/post/<int:post_id>/update',  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       "static/images/" + post.image_1))
                post.image_1 = photos.save(request.files.get(
                    'image_1'), name=secrets.token_hex(10) + ".")
            except:
                post.image_1 = photos.save(request.files.get(
                    'image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       "static/images/" + post.image_2))
                post.image_2 = photos.save(request.files.get(
                    'image_2'), name=secrets.token_hex(10) + ".")
            except:
                post.image_2 = photos.save(request.files.get(
                    'image_2'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash('Your post was updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('add_post.html', title='Update Post', form=form)


@app.route('/post/<int:post_id>/delete',  methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
