from flask import Blueprint, render_template, abort, url_for
from jinja2 import TemplateNotFound
import logging

home_page_bp = Blueprint('home_page_bp', __name__, template_folder='templates')


@home_page_bp.route('/')
def home_page():
    try:
        logging.info("Someone accessed the home page!")
        return render_template(
            'home.html',
            login_page=   url_for('auth_bp.login'),
            logout_page=  url_for('auth_bp.logout'),
            sign_up_page= url_for('auth_bp.sign_up'),
            change_password_page=url_for('auth_bp.change_password')
       )
    except TemplateNotFound:
        abort(404)
