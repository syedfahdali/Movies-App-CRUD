from flask import Blueprint, render_template, abort, url_for, request
from jinja2 import TemplateNotFound
import requests
import logging

home_page_bp = Blueprint('home_page_bp', __name__, template_folder='templates')



@home_page_bp.route('/')
def home_page():
    try:
        logging.info("Someone accessed the home page!")
        
        # Example movie IDs
        movie_ids = [1, 2, 3, 4, 5]

        # Function to fetch movie data for a given ID
        def get_movie_tile(movie_id):
            try:
                # Make a GET request to the API to fetch movie details
                response = requests.get(f'http://127.0.0.1/get_movie?id={movie_id}')
                if response.status_code == 200:
                    # Extract movie data from the response
                    movie_data = response.json()
                    # Return movie information
                    return movie_data.get('movie')
                else:
                    # Return None if the request was not successful
                    return None
            except Exception as e:
                # Log any exceptions
                logging.error(e)
                return None
        
        # Render the home.html template with movie IDs and function to fetch movie tiles
        return render_template(
            'home.html',
            movie_ids=movie_ids,
            get_movie_tile=get_movie_tile,
            login_page=url_for('auth_bp.login'),
            logout_page=url_for('auth_bp.logout'),
            sign_up_page=url_for('auth_bp.sign_up'),
            change_password_page=url_for('auth_bp.change_password'),
            
        )
        
    except TemplateNotFound:
        abort(404)
