from flask import Flask
from website.pages.home.home import home_page_bp
from website.pages.API.API import API_bp
from website.pages.auth.auth import auth_bp
from database.models import *  # Import all models, if this is not done, db.create_all() will not create the tables
from flask_login import LoginManager
from os import path


def create_app():
    app = Flask(__name__, instance_relative_config=False, static_folder='static', static_url_path='')

    app.config["SECRET_KEY"] = "99104e36d88579dfd4bd3c9c0fb2736351ec4fb5dc9c64c67a7009a24e20c998"
    app.config["SERVER_NAME"] = "127.0.0.1"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + path.join(path.abspath(path.dirname(__file__)), 'app.db')

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    @login_manager.user_loader
    def load_user(_id):
        return db.session.query(User).filter_by(id=_id).first()

    try:
        with app.app_context():
            db.create_all()

        app.register_blueprint(home_page_bp)
        app.register_blueprint(API_bp)
        app.register_blueprint(auth_bp)
        return app

    except Exception as e:
        raise ValueError("Failed to create app: " + str(e))
