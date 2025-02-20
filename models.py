from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    date = db.Column(db.Date)
    content = db.Column(db.String())

    def __repr__(self):
        return f"Post ({self.id} | {self.title} | {self.date})"