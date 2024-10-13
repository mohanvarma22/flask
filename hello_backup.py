from flask import Flask,render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin,login_user,LoginManager,logout_user,current_user,login_required

#create a flask instance
app=Flask(__name__)
#add database
#old sql db
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Users.db'
#new mysql db  'mysql://username:password@localhost/db_name
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1234@localhost/our_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#secret key
app.config['SECRET_KEY']="you are not supposed to know"
#initialize a database
db=SQLAlchemy(app)
migrate=Migrate(app, db)

#flask login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#class login form
class LoginForm(FlaskForm):
    username=StringField("username",validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])
    submit=SubmitField("Submit")


#Create Login Page
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Successful")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password - try again")
        else:
            flash("that user doesnt exist")
    return render_template('login.html',form=form)
#create logout page
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for('login'))
#Create dashboard page
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    
    return render_template('dashboard.html')

class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255))
    content=db.Column(db.Text)
    author=db.Column(db.String(255))
    date_posted=db.Column(db.DateTime,default=datetime.utcnow)
    slug=db.Column(db.String(255))
#Create posts Form
class PostForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    content=StringField("Content",validators=[DataRequired()],widget=TextArea())
    author=StringField("Author",validators=[DataRequired()])
    slug=StringField("Slug",validators=[DataRequired()])
    submit=SubmitField("Submit")

@app.route('/posts/<int:id>')
def post(id):
    post=Posts.query.get_or_404(id)
    return render_template('post.html',post=post)


@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html",posts=posts)

@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete=Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Blog Post Was Deleted")
        posts=Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',posts=posts)
    except:
        flash("There was a problem deleting the post please try again")
        posts=Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',posts=posts)
    
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
# @login_required easy way
@login_required
def edit_post(id):
    post=Posts.query.get_or_404(id)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.author=form.author.data
        post.slug=form.slug.data
        post.content=form.content.data
        #Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated successfully")
        return redirect(url_for('post',id=post.id))
    form.title.data=post.title
    form.author.data=post.author
    form.slug.data=post.slug
    form.content.data=post.content
    return render_template("edit_post.html",form=form)

@app.route('/add-post',methods=['GET','POST'])
#@login_required easiest way to redirect the user if he is not logged in
def add_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Posts(title=form.title.data,content=form.content.data,author=form.author.data,slug=form.slug.data)
        form.title.data=''
        form.content.data=''
        form.author.data=''
        form.slug.data=''
        #add post data to database
        db.session.add(post)
        db.session.commit()
        flash("Blog post submitted")
    return render_template("add_post.html",form=form)
#Create Model
class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    favorite_color=db.Column(db.String(100))
    date_added=db.Column(db.DateTime,default=datetime.utcnow)
    #passsword hash
    password_hash=db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('Password is not readable')
    
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)


    #create a string
    def __repr__(self):
        return '<Name %r>' %self.name
    
@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name=None
    form=UserForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #hash the password
            hashed_pw=generate_password_hash(form.password_hash.data,"pbkdf2:sha256")
            user=Users(username=form.username.data,name=form.name.data,email=form.email.data,favorite_color=form.favorite_color.data,password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.username.data=''
        form.email.data=''
        form.favorite_color.data=''
        form.password_hash=''
        flash("been added successfully")
    our_users=Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,name=name,our_users=our_users)
    
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    user_to_delete=Users.query.get_or_404(id)
    name=None
    form=UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")
        our_users=Users.query.order_by(Users.date_added)
        return render_template("add_user.html",form=form,name=name,our_users=our_users)
    except:
        flash("error!")
        return render_template("add_user.html",form=form,name=name,our_users=our_users)
#create a user form
class UserForm(FlaskForm):
    name=StringField("What's Your name babes",validators=[DataRequired()])#validators kuda chala untay such as email,equalto extra
    username=StringField("username",validators=[DataRequired()])
    email=StringField("email",validators=[DataRequired()])
    favorite_color=StringField("Favorite color")
    password_hash=PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2',message='Passwords Must match')])
    password_hash2=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField("Submit")

#Update database record
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update=Users.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.email=request.form['email']
        name_to_update.favorite_color=request.form['favorite_color']
        name_to_update.username=request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html",form=form,name_to_update=name_to_update)
        except:
            flash("Update Failed")
            return render_template("update.html",form=form,name_to_update=name_to_update)
    else:
         return render_template("update.html",form=form,name_to_update=name_to_update,id=id)
    
class PasswordForm(FlaskForm):
    email=StringField("What's Your Email",validators=[DataRequired()])#validators kuda chala untay such as email,equalto extra
    password_hash=PasswordField("Enter your password",validators=[DataRequired()])
    submit=SubmitField("Submit")
#create a form class
class NamerForm(FlaskForm):
    name=StringField("What's Your name babes",validators=[DataRequired()])#validators kuda chala untay such as email,equalto extra
    submit=SubmitField("Submit")
    #ila chala fields  vadkochu from documentary
    #file field
    #hidden field ila chala untay

#route decorator
@app.route('/')

# def index():
#     return "<h1> Hola </h1>"

def index():
    first_name="Mohan varma"
    # stuff = "This is <strong>Bold</strong>"
    favorite_food=["Biryani","Tandoori","Chapathi-chicken"]
    return render_template('index.html',first_name=first_name,favorite_food=favorite_food)
                        #  stuff=stuff  

@app.route('/user/<name>')

def user(name):
    return render_template('user.html',user_name=name)

#Create custom error pages

#invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

#internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500

@app.route('/name',methods=['GET','POST'])
def name():
    name=None
    form=NamerForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash("submitted the form successfully")
    return render_template("name.html",name=name,form=form)

@app.route('/test_pw',methods=['GET','POST'])
def test_pw():
    email=None
    password=None
    pw_to_check=None
    passed=None
    form=PasswordForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password_hash.data

        form.email.data=''
        form.password_hash.data=''

        pw_to_check=Users.query.filter_by(email=email).first()
        passed=check_password_hash(pw_to_check.password_hash,password)
        #flash("submitted the form successfully")
    return render_template("test_pw.html",email=email,password=password,form=form,pw_to_check=pw_to_check,passed=passed)

if __name__ == "__main__":
    app.run(debug=True)