from dataclasses import dataclass, field
from datetime import datetime


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
