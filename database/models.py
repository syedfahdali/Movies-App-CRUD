from flask_login import UserMixin
from database.database import db
from datetime import datetime

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(300))
    director_first_name = db.Column(db.String(100))
    director_last_name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    actors_first_name = db.Column(db.String(100))
    actors_last_name = db.Column(db.String(100))
    actor_role = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    movie_status = db.Column(db.String(50))
    reviews = db.relationship('Review', backref='movie', lazy=True, cascade='all, delete-orphan')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password = db.Column(db.String(150), nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)





class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
