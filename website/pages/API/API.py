from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
import logging
from database.models import Movie, Category, db,Review
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

UPLOAD_FOLDER = 'uploads'
API_bp = Blueprint('API_bp', __name__, template_folder='templates')

# Route to render the create movie form
@API_bp.route('/add_movie', methods=['GET'])
def add_movie_form():
    return render_template('create_movie.html')

# Route to create a new movie
@API_bp.route('/create_movie', methods=['POST'])
def create_movie():
    try:
        movie_title = request.form.get("movie_name")
        director_first_name = request.form.get("director_first_name")
        director_last_name = request.form.get("director_last_name")
        year = request.form.get("year")
        actors_first_name = request.form.get("actors_first_name")
        actors_last_name = request.form.get("actors_last_name")
        actor_role = request.form.get("actor_role")
        category_name = request.form.get("category_name")
        movie_status = request.form.get("movie_status")
        image_url = request.form.get("image_url")  # Add this line to get the image URL from the form

        # Check for all fields
        if not all([movie_title, director_first_name, director_last_name, year, actors_first_name, actors_last_name, actor_role, category_name, movie_status, image_url]):
            flash("All fields are required", "error")
            return redirect(url_for('API_bp.add_movie_form'))

        # Check if the category already exists
        category = db.session.query(Category).filter_by(name=category_name).first()

        # If category does not exist, create a new category
        if category is None:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

        # Create a new movie with the category's ID
        movie = Movie(
            category_id=category.id,
            movie_status=movie_status,
            name=movie_title,
            year=year,
            director_first_name=director_first_name,
            director_last_name=director_last_name,
            actors_first_name=actors_first_name,
            actors_last_name=actors_last_name,
            actor_role=actor_role,
            image_url=image_url  # Assign the image URL directly to the movie object
        )

        db.session.add(movie)
        db.session.commit()

        flash(f"Movie added: {movie.name}", "success")
        return redirect(url_for('home_page_bp.home_page'))
    except Exception as e:
        logging.exception(e)
        flash("An error occurred while adding the movie", "error")
        return redirect(url_for('API_bp.add_movie_form'))

# Route to render the delete movie form
@API_bp.route('/delete_movie', methods=['GET'])
def delete_movie_page():
    return render_template('delete_movie.html')

# Route to delete a movie


@API_bp.route('/get_all_movies', methods=['GET'])
def get_all_movies():
    try:
        # Query all movies from the database
        movies = db.session.query(Movie).all()

        # Extract the names of all movies
        movie_list = [{"id": movie.id, "name": movie.name, "image_url":movie.image_url} for movie in movies]
        return {"movies": movie_list}
    except Exception as e:
        logging.exception(e)
        return {"error": "Internal Server Error"}, 500

@API_bp.route('/get_movie', methods=['GET'])
def get_movie():
    try:
        # Get the movie ID from the request arguments
        movie_id = request.args.get("id")

        # Check if the movie ID is provided
        if movie_id is None:
            return {"error": "Movie ID is missing"}, 400

        # Convert movie ID to an integer
        movie_id = int(movie_id)

        # Query the movie from the database based on its ID
        movie = db.session.query(Movie).filter_by(id=movie_id).first()
        category= db.session.query(Category).filter_by(id=movie_id).first()
        # Check if the movie exists
        if movie and category:
            return {"movie": {
                    "name": movie.name,
                    "image_url": movie.image_url,
                    "director_first_name": movie.director_first_name,
                    "director_last_name": movie.director_last_name,
                    "year": movie.year,
                    "actors_first_name": movie.actors_first_name,
                    "actors_last_name": movie.actors_last_name,
                    "actor_role": movie.actor_role,
                    "movie_status": movie.movie_status
                },
                "category":{
                    "name": category.name
                }
                }
        else:
            return {"error": "Movie not found"}, 404
    except ValueError:
        return {"error": "Invalid movie ID"}, 400
    except Exception as e:
        logging.exception(e)
        return {"error": "Internal Server Error"}, 500

@API_bp.route('/update_movie', methods=['GET', 'POST'])
def update_movie():
    if request.method == 'GET':
        return render_template('update_movie.html')
    
    try:
        movie_id = request.form.get("movie_id")
        movie = db.session.query(Movie).filter_by(id=movie_id).first()

        # Check if the movie exists
        if not movie:
            flash("Movie not found", "error")
            return redirect(url_for('API_bp.update_movie'))

        # Update the movie details if provided
        if 'movie_name' in request.form:
            movie.name = request.form.get("movie_name")
        if 'director_first_name' in request.form:
            movie.director_first_name = request.form.get("director_first_name")
        if 'director_last_name' in request.form:
            movie.director_last_name = request.form.get("director_last_name")
        if 'year' in request.form:
            movie.year = request.form.get("year")
        if 'actors_first_name' in request.form:
            movie.actors_first_name = request.form.get("actors_first_name")
        if 'actors_last_name' in request.form:
            movie.actors_last_name = request.form.get("actors_last_name")
        if 'actor_role' in request.form:
            movie.actor_role = request.form.get("actor_role")
        if 'category_name' in request.form:
            category_name = request.form.get("category_name")
            category = db.session.query(Category).filter_by(name=category_name).first()
            if category is None:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()
            movie.category_id = category.id
        if 'movie_status' in request.form:
            movie.movie_status = request.form.get("movie_status")
        if 'image_url' in request.form:
            movie.image_url = request.form.get("image_url")

        db.session.commit()

        flash(f"Movie updated: {movie.name}", "success")
        return redirect(url_for('home_page_bp.home_page'))
    except Exception as e:
        logging.exception(e)
        flash("An error occurred while updating the movie", "error")
        return redirect(url_for('API_bp.update_movie'))
@API_bp.route('/movie_details', methods=['GET'])
def movie_details():
    try:
        movie_id = request.args.get("id")
        if movie_id is None:
            return {"error": "Movie ID is missing"}, 400
        
        # Convert movie_id to an integer
        movie_id = int(movie_id)
        
        movie = db.session.query(Movie).filter_by(id=movie_id).first()
        category = db.session.query(Category).filter_by(id=movie_id).first()
        reviews = Review.query.filter_by(movie_id=movie_id).all()

        if movie and category:
            return render_template('movie_details.html', movie=movie, category=category, reviews=reviews)
        else:
            flash("Movie not found", "error")
            return redirect(url_for('home_page_bp.home_page'))
    except ValueError:
        return {"error": "Invalid movie ID"}, 400
    except Exception as e:
        logging.exception(e)
        flash("An error occurred while retrieving movie details", "error")
        return redirect(url_for('home_page_bp.home_page'))



@API_bp.route('/submit_review', methods=['POST'])
def submit_review():
    # Check if the request content type is JSON
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({"error": "Content-Type must be 'application/json'"}), 415

    # Get JSON data from the request
    data = request.json

    # Extract user_id, movie_id, and content from the JSON data
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    content = data.get('content')

    # Check if all fields are provided
    if not user_id or not movie_id or not content:
        return jsonify({"error": "All fields are required"}), 400

    # Create and add the review to the database
    review = Review(user_id=user_id, movie_id=movie_id, content=content)
    db.session.add(review)
    db.session.commit()

    # Redirect to the movie details page
    return redirect(url_for('API_bp.movie_details', movie_id=movie_id))



@API_bp.route('/delete_review', methods=['POST'])
@login_required
def delete_review():
    try:
        review_id = request.json.get("review_id")

        if not review_id:
            return jsonify({"error": "Review ID is required"}), 400

        review_id = int(review_id)
        review = Review.query.get(review_id)

        if review and review.user_id == current_user.id:
            db.session.delete(review)
            db.session.commit()
            return jsonify({"message": "Review deleted successfully"}), 200
        else:
            return jsonify({"error": "Review not found or you do not have permission to delete this review"}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred while deleting the review"}), 500



@API_bp.route('/delete_movie', methods=['POST'])
def delete_movie():
    try:
        movie_id = request.form.get("movie_id")

        # Check if the movie ID is provided
        if not movie_id:
            flash("Movie ID is required", "error")
            return redirect(url_for('API_bp.delete_movie_page'))

        # Convert movie ID to an integer
        movie_id = int(movie_id)

        # Query the movie from the database based on its ID
        movie = db.session.query(Movie).filter_by(id=movie_id).first()

        # Check if the movie exists
        if movie:
            db.session.delete(movie)
            db.session.commit()
            flash(f"Movie with ID {movie_id} has been deleted", "success")
        else:
            flash("Movie not found", "error")

        return redirect(url_for('home_page_bp.home_page'))
    except Exception as e:
        logging.exception(e)
        flash("An error occurred while deleting the movie", "error")
        return redirect(url_for('API_bp.delete_movie_page'))