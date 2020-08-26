from flask import request, render_template
from flaskblog import app
from flaskblog.models import Post


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('index.html', posts=posts)
