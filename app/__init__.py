from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from pymongo import ASCENDING
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

mongo = PyMongo()
login = LoginManager()
login.login_view = 'authentication.login'
login.login_message = 'Please log in to access this page.'
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    login.init_app(app)
    mongo.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        mongo.db.users.create_index([('username', ASCENDING)], unique=True)
        mongo.db.user_requests.create_index([('username', ASCENDING)], unique=True)
        mongo.db.trackers.create_index([('title', ASCENDING)], unique=True)
        
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.authentication import bp as authentication_bp
    app.register_blueprint(authentication_bp, url_prefix='/auth')
    from app.trackerapp import bp as trackerapp_bp
    app.register_blueprint(trackerapp_bp)
    from app.projects import bp as project_bp
    app.register_blueprint(project_bp)
    if not app.debug:
        # ...

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/vid.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('log startup')
    return app


from app import usermodel, tracker, projectmodel



