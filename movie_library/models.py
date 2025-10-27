from dataclasses import dataclass, field
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask import current_app


@dataclass
class Movie:
    """
    A class to represent a movie.

    Attributes:
        _id (str): The movie's unique ID.
        title (str): The movie's title.
        director (str): The movie's director.
        year (int): The year the movie was released.
        cast (list[str]): A list of the movie's cast members.
        series (list[str]): A list of the series the movie belongs to.
        last_watched (datetime): The date the movie was last watched.
        rating (float): The movie's rating.
        tags (list[str]): A list of tags associated with the movie.
        description (str): The movie's description.
        video_link (str): A link to the movie's video.
        image_link (str): A link to the movie's image.
    """


    _id: str
    title: str
    director: str
    year: int
    cast: list[str] = field(default_factory=list)
    series: list[str] = field(default_factory=list)
    last_watched: datetime = None
    rating: float = 0.0
    tags: list[str] = field(default_factory=list)
    description: str = None
    video_link: str = None
    image_link: str = None


@dataclass
class User:
    """
    A class to represent a user.

    Attributes:
        _id (str): The user's unique ID.
        email (str): The user's email address.
        password (str): The user's hashed password.
        movies (list[str]): A list of movie IDs in the user's library.
    """

    _id: str
    email: str
    password: str
    movies: list[str] = field(default_factory=list)  # List of Movie IDs

    def get_reset_token(self, expires_sec=1800):
        """
        Generates a password reset token for the user.

        Args:
            expires_sec (int): The expiration time in seconds. Default is 1800 seconds (30 minutes).

        Returns:
            str: The generated token.
        """
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self._id})
    
    @staticmethod
    def verify_reset_token(token):
        """
        Verifies a password reset token.

        Args:
            token (str): The token to verify.

        Returns:
            str: The user ID associated with the token.
        """
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, max_age=1800)["user_id"]
        except:
            return None
        return User(**current_app.db.user.find_one({"_id": user_id}))
    

