from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

#search form
class SearchForm(FlaskForm):
    searched=StringField("Searched",validators=[DataRequired()])
    submit=SubmitField("Submit")

#login form
class LoginForm(FlaskForm):
    username=StringField("username",validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])
    submit=SubmitField("Submit")

#Create posts Form
class PostForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    # content=StringField("Content",validators=[DataRequired()],widget=TextArea())
    author=StringField("Author")
    content=CKEditorField('Content',validators=[DataRequired()])
    slug=StringField("Slug",validators=[DataRequired()])
    submit=SubmitField("Submit")

#create a user form
class UserForm(FlaskForm):
    name=StringField("What's Your name babes",validators=[DataRequired()])#validators kuda chala untay such as email,equalto extra
    username=StringField("username",validators=[DataRequired()])
    email=StringField("email",validators=[DataRequired()])
    favorite_color=StringField("Favorite color")
    about_author=TextAreaField("About Author")
    password_hash=PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2',message='Passwords Must match')])
    password_hash2=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField("Submit")

class PasswordForm(FlaskForm):
    email=StringField("What's Your Email",validators=[DataRequired()])#validators kuda chala untay such as email,equalto extra
    password_hash=PasswordField("Enter your password",validators=[DataRequired()])
    submit=SubmitField("Submit")

#create a form class
class NamerForm(FlaskForm):
    name=StringField("What's Your name babes",validators=[DataRequired()])#validators kuda chala untay such as email,equalto extra
    submit=SubmitField("Submit")