import os
from datetime import datetime
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

from movie_library.routes import pages

load_dotenv()


def create_app():
    """
    Creates and configures the Flask application.

    This function initializes the Flask app, loads configuration from environment
    variables, connects to the MongoDB database, and registers the blueprints.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY environment variable is required. "
            "Generate one with `python -c \"import secrets; print(secrets.token_urlsafe(32))\"` "
            "and set it in your environment or .env file."
        )
    app.config["SECRET_KEY"] = secret_key
    app.db = MongoClient(app.config["MONGODB_URI"])["movie_watchlist"]

    @app.context_processor
    def inject_current_year():
        return {"current_year": datetime.now().year}

    app.register_blueprint(pages)
    return app
