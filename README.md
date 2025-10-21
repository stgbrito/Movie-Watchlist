# Movie Watchlist

A simple web application for managing your movie watchlist.

## Features

- User registration and login
- Add movies to your watchlist
- Edit movie details
- Rate movies
- Mark movies as watched
- Dark mode toggle

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/movie-watchlist.git
   cd movie-watchlist
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**

   Create a `.env` file in the root directory and add the following environment variables:

   ```
   MONGODB_URI=<your_mongodb_uri>
   SECRET_KEY=<your_secret_key>
   ```

   You can generate a secret key with the following command:

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Run the application:**

   ```bash
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000`.

## Usage

1. Register for a new account.
2. Log in to your account.
3. Add movies to your watchlist.
4. Click on a movie to view its details, edit it, rate it, or mark it as watched.
5. Use the toggle switch to change the theme.
