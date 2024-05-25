from flask_login import UserMixin
from database.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    movie_status = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    director_first_name = db.Column(db.Text, nullable=False)
    director_last_name = db.Column(db.Text, nullable=False)
    actors_first_name = db.Column(db.Text, nullable=False)
    actors_last_name = db.Column(db.Text, nullable=False)
    actor_role = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
