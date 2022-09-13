from flask_sqlalchemy import SQLAlchemy

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