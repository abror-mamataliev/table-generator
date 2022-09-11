from flask import Flask
from os.path import dirname

from .blueprint import register_blueprints
from routes import *


def create_app(type: str = "prod") -> Flask:
    """
        Create a Flask app instance.

        :param type: The type of app to create. Can be "prod" or "dev".
        :return: The Flask app instance.
    """

    app: Flask = Flask(dirname(dirname(__file__)))
    app.config.from_object(f"config.{type.capitalize()}Config")

    register_blueprints(app)

    return app
