from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, login_user, logout_user, current_user
from models import db, Post, User
from config import Config
from datetime import datetime
from markdown import markdown
from copy import deepcopy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    if user_id == "None":
        return None
    return User.query.get(int(user_id))

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

DEFAULT_POST_TITLE = "Unnamed post"
DEFAULT_POST_CONTENT = "No post content was provided."

@app.route("/")
def main():
    return redirect("/post-list")

@app.route("/post/<int:post_id>", methods=["GET"])
def post(post_id):
    post = deepcopy(Post.query.get(post_id))
    post.content = markdown(post.content)
    return render_template("post.html", post=post)

@app.route("/post-editor/<int:post_id>", methods=["GET"])
def post_editor(post_id):
    if not current_user.is_admin:
        return redirect("/")
    
    post = Post.query.get(post_id)
    return render_template("post-editor.html", post=post, alert="")

@app.route("/update-post/<int:post_id>", methods=["GET", "POST"])
def update_post(post_id):
    if not current_user.is_admin:
        return redirect("/")
    
    post = Post.query.get(post_id)
    
    title = request.form.get("title")
    if title is None or title == "":
        title = DEFAULT_POST_TITLE
    
    date = request.form.get("date")
    if date is None:
        date = datetime.today()
    else:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    
    content = request.form.get("content")
    if content is None or content == "":
        content = DEFAULT_POST_CONTENT
    
    post.title = title
    post.date = date
    post.content = content
    db.session.commit()
    
    return redirect("/post-list")

@app.route("/post-list", methods=["GET"])
def post_list():
    posts = Post.query.all()
    
    return render_template("post-list.html", posts=posts)

@app.route("/delete-post/<int:post_id>", methods=["GET"])
def delete_post(post_id):
    if not current_user.is_admin:
        return redirect("/")
    
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect("/post-list")

@app.route("/create-post", methods=["POST", "GET"])
def create_post():
    if not current_user.is_admin:
        return redirect("/")
    
    title = DEFAULT_POST_TITLE
    date = datetime.today()
    content = DEFAULT_POST_CONTENT
    
    post = Post(title=title, date=date, content=content)
    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/post-editor/{post.id}")

@app.route("/registration-form")
def registration_form():
    return render_template("registration-form.html", alert_message="")

@app.route("/register-user", methods=["POST", "GET"])
def register_user():
    username = request.form.get("username")
    password = request.form.get("password")
    is_admin_string = request.form.get("is-admin")

    print(username, password, is_admin_string)

    if username is None or len(username) < 4 or 32 < len(username):
        alert_message = "The username must be between 4 and 32 characters long"
        return render_template("registration-form.html", alert_message=alert_message)
    
    username_taken = User.query.filter_by(username=username).first()
    if username_taken:
        alert_message = "Username is already taken"
        return render_template("registration-form.html", alert_message=alert_message)
    
    
    if password is None or len(password) < 8 or 32 < len(password):
        alert_message = "The password must be between 8 and 32 characters long"
        return render_template("registration-form.html", alert_message=alert_message)
    password_hash = generate_password_hash(password)

    
    is_admin = bool(is_admin_string == "on")
    
    user = User(
        username=username,
        password_hash=password_hash,
        is_admin=is_admin,
    )
    
    db.session.add(user)
    db.session.commit()

    login_user(user)

    return redirect("/post-list")

@app.route("/login-form")
def login_form():
    return render_template("login-form.html", alert_message="")

@app.route("/login-user", methods=["POST", "GET"])
def login_user_():
    username = request.form.get("username")
    password = request.form.get("password")

    print(username, password)

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return redirect("/post-list")
    alert_message = "Wrong username or password"
    return render_template("login-form.html", alert_message=alert_message)

@app.route("/logout-user", methods=["POST", "GET"])
def logout_user_():
    logout_user()
    return redirect("/")