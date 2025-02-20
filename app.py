from flask import Flask, redirect, render_template, request
from models import db, Post
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

DEFAULT_POST_TITLE = "Unnamed post"
DEFAULT_POST_CONTENT = "No post content was provided."

@app.route("/")
def main():
    return redirect("/post-list")

@app.route("/post/<int:post_id>", methods=["GET"])
def post(post_id):
    post = Post.query.get(post_id)
    return render_template("post.html", post=post)

@app.route("/post-editor/<int:post_id>", methods=["GET"])
def post_editor(post_id):
    post = Post.query.get(post_id)
    return render_template("post-editor.html", post=post)

@app.route("/update-post/<int:post_id>", methods=["GET", "POST"])
def update_post(post_id):
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
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect("/post-list")

@app.route("/create-post", methods=["POST", "GET"])
def create_post():
    title = DEFAULT_POST_TITLE
    date = datetime.today()
    content = DEFAULT_POST_CONTENT
    
    post = Post(title=title, date=date, content=content)
    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/post-editor/{post.id}")