from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    date = db.Column(db.Date)
    content = db.Column(db.String())

    def __repr__(self):
        return f"Post ({self.id} | {self.title} | {self.date})"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024), nullable="False")
    is_admin = db.Column(db.Boolean)

    def __repr__(self):
        return f"User ({self.id} | {self.username} | {self.is_admin})"