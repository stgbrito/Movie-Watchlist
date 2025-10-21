from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    TextAreaField,
    URLField,
    PasswordField,
)
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo


class MovieForm(FlaskForm):
    """
    A form for adding or editing a movie.

    Attributes:
        title (StringField): The title of the movie.
        director (StringField): The director of the movie.
        year (IntegerField): The year the movie was released.
        submit (SubmitField): The submit button.
    """

    title = StringField("Title", validators=[InputRequired()])
    director = StringField("Director", validators=[InputRequired()])

    year = IntegerField(
        "Year",
        validators=[
            InputRequired(),
            NumberRange(min=1878, message="Please enter a year in the format YYYY."),
        ],
    )

    submit = SubmitField("Add Movie")


class StringListField(TextAreaField):
    """
    A custom field for entering a list of strings, separated by newlines.
    """

    def _value(self):
        if self.data:
            return "\n".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        """
        Processes the form data and converts it to a list of strings.

        Args:
            valuelist (list): The list of values from the form.
        """
        if valuelist and valuelist[0]:
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        else:
            self.data = []


class ExtendedMovieForm(MovieForm):
    """
    An extended form for adding or editing a movie, with additional fields.

    Attributes:
        cast (StringListField): The cast of the movie.
        series (StringListField): The series the movie belongs to.
        tags (StringListField): The tags associated with the movie.
        description (TextAreaField): The description of the movie.
        video_link (URLField): The link to the movie's video.
        image_link (URLField): The link to the movie's image.
        submit (SubmitField): The submit button.
    """

    cast = StringListField("Cast")
    series = StringListField("Series")
    tags = StringListField("Tags")
    description = TextAreaField("Description")
    video_link = URLField("Video link")
    image_link = URLField("Image link")

    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    """
    A form for user registration.

    Attributes:
        email (StringField): The user's email address.
        password (PasswordField): The user's password.
        confirm_password (PasswordField): The user's password confirmation.
        submit (SubmitField): The submit button.
    """

    email = StringField(
        "Email",
        validators=[InputRequired(), Email()],
        filters=[lambda value: value.strip().lower() if isinstance(value, str) else value],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    """
    A form for user login.

    Attributes:
        email (StringField): The user's email address.
        password (PasswordField): The user's password.
        submit (SubmitField): The submit button.
    """

    email = StringField(
        "Email",
        validators=[InputRequired(), Email()],
        filters=[lambda value: value.strip().lower() if isinstance(value, str) else value],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
        ],
    )
    submit = SubmitField("Log in")
