from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_1 = FileField('Upload Image', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])
    image_2 = FileField('Upload Image', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Comment')
