from flask import (
    Blueprint,
    Flask
)


table = Blueprint("table", __name__)


def register_blueprints(app: Flask) -> None:
    """
        Register all blueprints for the application

        :param app: Flask application
    """

    app.register_blueprint(table)
