from flask import Flask, redirect, render_template, request
from datetime import date as current_date

app = Flask(__name__)

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
    content = request.form.get("content", "No post content was provided.")
    print(title, date, content, sep="\n")
    
    return redirect("/")