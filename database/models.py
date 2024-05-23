from flask_login import UserMixin
from database.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


# example how to create a table called movie with the columns id, category_id and name
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # nullable=False means that it always must have a value
    # category_id is a foreign key that references a category in the Category table
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # this can only contain strings from the MovieStatus strenum, this has been added as an example and does not
    # have to be used
    movie_status = db.Column(db.Text, nullable=False)

    name = db.Column(db.Text, nullable=False)


# example how to create a table called category with the columns id and name
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # unique=True enforces that no two categories can have the same name
    name = db.Column(db.Text, nullable=False, unique=True)
