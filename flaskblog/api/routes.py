from flaskblog.models import User, Post, Comment
from flask_restful import Api, Resource, abort, fields, marshal_with
from flaskblog import app

api = Api(app)

user_resource_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'image_file': fields.String
}

post_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'date_posted': fields.DateTime,
    'image_1': fields.String,
    'image_2': fields.String,
    'user_id': fields.Integer
}

comment_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_added': fields.DateTime,
    'content': fields.String,
    'post_id': fields.Integer
}

class AllUsers(Resource):
    @marshal_with(user_resource_fields)
    def get(self):
        result = User.query.all()
        return result

class SingleUser(Resource):
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        result = User.query.filter_by(id=user_id).first()
        return result

class AllPosts(Resource):
    @marshal_with(post_resource_fields)
    def get(self):
        result = Post.query.all()
        return result

class SinglePost(Resource):
    @marshal_with(post_resource_fields)
    def get(self, post_id):
        result = Post.query.filter_by(id=post_id).first()
        return result

class AllComments(Resource):
    @marshal_with(comment_resource_fields)
    def get(self):
        result = Comment.query.all()
        return result

class SingleComment(Resource):
    @marshal_with(comment_resource_fields)
    def get(self, comment_id):
        result = Comment.query.filter_by(id=comment_id).first()
        return result


api.add_resource(AllUsers, '/api/v1/resource/users/all')
api.add_resource(SingleUser, '/api/v1/resource/users/<int:user_id>')
api.add_resource(AllPosts, '/api/v1/resource/posts/all')
api.add_resource(SinglePost, '/api/v1/resource/posts/<int:post_id>')
api.add_resource(AllComments, '/api/v1/resource/comments/all')
api.add_resource(SingleComment, '/api/v1/resource/comments/<int:comment_id>')

