import uuid
import datetime
import functools
from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    current_app,
    url_for,
    flash,
)
from dataclasses import asdict
from movie_library.forms import MovieForm, ExtendedMovieForm, RegisterForm, LoginForm, ResetPasswordForm, RequestResetForm, UpdateAccountForm
from movie_library.models import Movie, User
from passlib.hash import pbkdf2_sha256
from flask_mail import Message
from movie_library import mail


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

def login_required(route):
    """
    A decorator to ensure a user is logged in before accessing a route.

    If the user is not logged in, they are redirected to the login page.

    Args:
        route (function): The route to protect.

    Returns:
        function: The decorated route.
    """

    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))

        return route(*args, **kwargs)

    return route_wrapper


@pages.route("/")
@login_required
def index():
    """
    Renders the user's movie watchlist.

    Returns:
        str: The rendered HTML of the index page.
    """
    user_data = current_app.db.user.find_one({"email": session["email"]})
    user = User(**user_data)

    movie_data = current_app.db.movie.find({"_id": {"$in": user.movies}})
    movies = [Movie(**data) for data in movie_data]
    return render_template(
        "index.html",
        title="Movies Watchlist",
        movies_data=movies,
    )


@pages.route("/register", methods=["GET", "POST"])
def register():
    """
    Renders the registration page and handles user registration.

    If the user is already logged in, they are redirected to the index page.

    Returns:
        str: The rendered HTML of the registration page.
    """
    if session.get("email"):
        return redirect(url_for(".index"))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )

        current_app.db.user.insert_one(asdict(user))

        flash("User registered successfully!", "success")

        return redirect(url_for(".login"))

    return render_template(
        "register.html", title="Movies Watchlist - Register", form=form
    )

@pages.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders the login page and handles user login.

    If the user is already logged in, they are redirected to the index page.

    Returns:
        str: The rendered HTML of the login page.
    """
    if session.get("email"):
        return redirect(url_for(".index"))

    form = LoginForm()

    if form.validate_on_submit():
        user_data = current_app.db.user.find_one({"email": form.email.data})
        if not user_data:
            flash("Login failed. Please check your email and password.", category="danger")
            return redirect(url_for(".login"))
        
        user = User(**user_data)

        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_id"] = user._id
            session["email"] = user.email

            return redirect(url_for(".index"))
        
        flash("Login failed. Please check your email and password.", category="danger")

    return render_template("login.html", title="Movies Watchlist - Login", form=form)
            

@pages.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """
    Renders the account page and handles updating user account information.
    """
    form = UpdateAccountForm()

    if form.validate_on_submit():
        user_data = current_app.db.user.find_one({"email": session["email"]})
        user = User(**user_data)

        # Verify current password
        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            # Update email
            current_app.db.user.update_one(
                {"_id": user._id},
                {"$set": {"email": form.email.data}}
            )
            # Update session email
            session["email"] = form.email.data

            flash("Your account has been updated!", "success")
            return redirect(url_for(".account"))
        else:
            flash("Incorrect password. Please try again.", "danger")
    elif request.method == "GET":
        # Pre-fill the form with current user data
        form.email.data = session["email"]

    return render_template("account.html", title="Account", form=form)

@pages.route("/logout")
def logout():
    """
    Logs the user out and redirects to the login page.

    Returns:
        werkzeug.utils.redirect: A redirect to the login page.
    """
    current_theme = session.get("theme")
    session.clear()
    session["theme"] = current_theme

    return redirect(url_for(".login"))


def send_reset_email(user):
    """
    Sends a password reset email to the user.

    Args:
        user (User): The user to send the email to.
    """
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:
{url_for('pages.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)


@pages.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    """
    Renders the page to request a password reset and handles the form submission.
    """
    if session.get("email"):
        return redirect(url_for(".index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user_data = current_app.db.user.find_one({"email": form.email.data})
        if user_data:
            user = User(**user_data)
            send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for(".login"))
    
    return render_template("reset_request.html", title="Reset Password", form=form)

@pages.route("/reset_request/<token>", methods=["GET", "POST"])
def reset_token(token):
    """
    Renders the page to reset a user's password and handles the form submission.
    """
    if session.get("email"):
        return redirect(url_for(".index"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for(".reset_request"))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = pbkdf2_sha256.hash(form.password.data)
        current_app.db.user.update_one(
            {"_id": user._id}, 
            {"$set": {"password": hashed_password}}
        )
        flash("Your password has been updated! You can now log in.", "success")
        return redirect(url_for(".login"))
    return render_template("reset_token.html", title="Reset Password", form=form)



@pages.route("/add", methods=["GET", "POST"])
@login_required
def add_movie():
    """
    Renders the add movie page and handles adding a new movie.

    Returns:
        str: The rendered HTML of the add movie page.
    """
    form = MovieForm()

    if form.validate_on_submit():
        movie = Movie(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            director=form.director.data,
            year=form.year.data,
        )

        current_app.db.movie.insert_one(asdict(movie))
        current_app.db.user.update_one(
            {"_id": session["user_id"]}, {"$push": {"movies": movie._id}}
        )


        return redirect(url_for(".movie_added", _id=movie._id))

    return render_template(
        "new_movie.html",
        title="Movies Watchlist - Add Movie",
        form=form,
    )


@pages.route("/added/<string:_id>")
def movie_added(_id: str):
    """
    Renders a confirmation page after a movie has been added.

    Args:
        _id (str): The ID of the movie that was added.

    Returns:
        str: The rendered HTML of the movie added page.
    """
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    return render_template("movie_added.html", movie=movie)


@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
@login_required
def edit_movie(_id: str):
    """
    Renders the edit movie page and handles editing a movie.

    Args:
        _id (str): The ID of the movie to edit.

    Returns:
        str: The rendered HTML of the edit movie page.
    """
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    form = ExtendedMovieForm(obj=movie)
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.director = form.director.data
        movie.year = form.year.data
        movie.cast = form.cast.data
        movie.series = form.series.data
        movie.tags = form.tags.data
        movie.description = form.description.data
        movie.video_link = form.video_link.data
        movie.image_link = form.image_link.data

        current_app.db.movie.update_one({"_id": movie._id}, {"$set": asdict(movie)})

        return redirect(url_for(".movie", _id=movie._id))
    return render_template("movie_form.html", movie=movie, form=form)


@pages.get("/movie/<string:_id>")
def movie(_id: str):
    """
    Renders the movie details page.

    Args:
        _id (str): The ID of the movie to display.

    Returns:
        str: The rendered HTML of the movie details page.
    """
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    return render_template(
        "movie_details.html",
        title=f"Movies Watchlist - {movie.title}",
        movie=movie,
    )


@pages.get("/movie/<string:_id>/rate")
@login_required
def rate_movie(_id):
    """
    Rates a movie and redirects to the movie details page.

    Args:
        _id (str): The ID of the movie to rate.

    Returns:
        werkzeug.utils.redirect: A redirect to the movie details page.
    """
    rating = int(request.args.get("rating"))
    current_app.db.movie.update_one({"_id": _id}, {"$set": {"rating": rating}})

    return redirect(url_for(".movie", _id=_id))


@pages.get("/movie/<string:_id>/watch")
@login_required
def watch_today(_id):
    """
    Updates the last watched date of a movie to today and redirects to the movie details page.

    Args:
        _id (str): The ID of the movie to mark as watched.

    Returns:
        werkzeug.utils.redirect: A redirect to the movie details page.
    """
    current_app.db.movie.update_one(
        {"_id": _id}, {"$set": {"last_watched": datetime.datetime.today()}}
    )

    return redirect(url_for(".movie", _id=_id))


@pages.get("/toggle-theme")
def toggle_theme():
    """
    Toggles the theme between light and dark mode.

    Returns:
        werkzeug.utils.redirect: A redirect to the current page.
    """
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
    return redirect(request.args.get("current_page"))
