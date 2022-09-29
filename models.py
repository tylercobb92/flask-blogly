from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

default_img = "https://www.freeiconspng.com/uploads/user-login-icon-14.png"

def connect_db(app):
    db.app=app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name=db.Column(db.String, nullable=False)
    last_name=db.Column(db.String, nullable=False)
    image_url=db.Column(db.String, nullable=False, default=default_img)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # @property from solution: lookup how it works
    # @property
    # def friendly_date(self):
    #     return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")