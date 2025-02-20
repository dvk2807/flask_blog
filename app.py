from flask import Flask, redirect, render_template, request
from models import db, Post
from config import Config
from datetime import date as current_date, datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def main():
    return redirect("/post-creation")

@app.route("/post-creation")
def post_creation():
    return render_template("post-creation.html")

@app.route("/add-post", methods=["POST"])
def create():
    title = request.form.get("title", "Unnamed post")
    date = request.form.get("date", current_date)
    date = datetime.strptime(date, "%Y-%m-%d").date()
    content = request.form.get("content", "No post content was provided.")
    
    post = Post(title=title, date=date, content=content)
    db.session.add(post)
    db.session.commit()
    
    posts = Post.query.all()
    print(posts)
    
    return redirect("/")