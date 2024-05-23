from flask import Blueprint, request, abort
import logging
from database.models import Movie, Category, db

API_bp = Blueprint('API_bp', __name__)


# test url: http://127.0.0.1/create_movie?movie_status=PreProduction&movie_name=test&category_name=test2
@API_bp.route('/create_movie')
def create_movie():
    try:
        movie_status = request.args["movie_status"]
        movie_name = request.args["movie_name"]
        category_name = request.args["category_name"]

        # .first() returns None if no row could be found with the provided arguments
        category = db.session.query(Category).filter_by(name=category_name).first()

        # if category does not exist create a new category
        if category is None:
            category_object = Category(name=category_name)
            db.session.add(category_object)
            db.session.commit()

        # movie = Movie.create(category_id=category.id, movie_status=movie_status, name=movie_name)
        movie_object = Movie(category_id=category.id, movie_status=movie_status, name=movie_name)
        db.session.add(movie_object)
        db.session.commit()
        return {"response": f"movie added: {movie_object.name}"}
    except Exception as e:
        logging.exception(e)
        return {"response": "an error occurred"}


# test url: http://127.0.0.1/get_movie?movie_id=1
@API_bp.route('/get_movie')
def get_movie():
    try:
        movie_id = int(request.args["movie_id"])

        # there can only be one movie with a certain id so you can use .one() here. If no movie with this id exists it
        # will still throw an error
        movie = db.session.query(Movie).filter_by(id=movie_id).one()

        return {"movie": f"{movie.name}"}
    except Exception as e:
        logging.exception(e)
        return {"movie": "Not found"}
