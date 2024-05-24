from flask import Blueprint, request, render_template, redirect, url_for, flash
import logging
from database.models import Movie, Category, db
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'uploads'
API_bp = Blueprint('API_bp', __name__,template_folder='templates')

# Route to render the create movie form
@API_bp.route('/add_movie', methods=['GET'])
def add_movie_form():
    return render_template('create_movie.html')

# Route to create a new movie
@API_bp.route('/create_movie', methods=['POST'])
def create_movie():
    try:
        movie_status = request.form.get("movie_status")
        movie_name = request.form.get("movie_name")
        category_name = request.form.get("category_name")

        if not movie_status or not movie_name or not category_name:
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
        movie = Movie(category_id=category.id, movie_status=movie_status, name=movie_name)

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                movie.image_url = os.path.join(UPLOAD_FOLDER, filename)
            else:
                # If no image is selected, use default image
                movie.image_url = url_for('static', filename='images/default_image.jpg')

        db.session.add(movie)
        db.session.commit()

        flash(f"Movie added: {movie.name}", "success")
        return redirect(url_for('home_page_bp.home_page'))
    except Exception as e:
        logging.exception(e)
        flash("An error occurred while adding the movie", "error")
        return redirect(url_for('API_bp.add_movie_form'))


    
@API_bp.route('/get_all_movies', methods=['GET'])
def get_all_movies():
    try:
        # Query all movies from the database
        movies = db.session.query(Movie).all()

        # Extract the names of all movies
        movie_list = [{"id": movie.id, "name": movie.name} for movie in movies]
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

        # Check if the movie exists
        if movie:
            return {"movie": {"name": movie.name, "id": movie.id}}
        else:
            return {"error": "Movie not found"}, 404
    except ValueError:
        return {"error": "Invalid movie ID"}, 400
    except Exception as e:
        logging.exception(e)
        return {"error": "Internal Server Error"}, 500

@API_bp.route('/delete_movie', methods=['GET'])
def delete_movie_page():
    return render_template('delete_movie.html')