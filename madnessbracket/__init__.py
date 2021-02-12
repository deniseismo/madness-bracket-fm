from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from madnessbracket.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    """
    creates an instance of an app
    :param config_class: Config class file with all the configuration
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    return app
