import os
from datetime import datetime
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

from movie_library.routes import pages

load_dotenv()


def create_app():
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
