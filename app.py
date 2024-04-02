from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, login_required, current_user
import json

app = Flask(__name__)
app.secret_key = "-Pjp4.?MiZrR"

login_manager = LoginManager()
login_manager.init_app(app)

# Load example data from JSON files.
with open("./data/users.json") as f:
    users = json.load(f)

with open("./data/movies.json") as f:
    movies = json.load(f)

with open("./data/ratings.json") as f:
    ratings = json.load(f)

current_user = None


def get_average_rating(movie_id):
    """Define a helper function to calculate average rating for a movie."""
    movie_ratings = [rating for rating in ratings if rating["movie_id"] == movie_id]
    if movie_ratings:
        return sum(rating["rating"] for rating in movie_ratings) / len(movie_ratings)
    else:
        return f"There is no ratings yet for movie id: `{movie_id}`."


@app.route("/login", methods=["POST"])
def login():
    global current_user
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    for user in users:
        if user["email"] == data["email"] and user["password"] == data["password"]:
            current_user = user
            return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/movies", methods=["GET"])
def get_movies():
    """List all the movies from the movies db."""
    return jsonify(movies)


@app.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    for movie in movies:
        if movie["id"] == movie_id:
            movie["average_rating"] = get_average_rating(movie_id)
            return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404


@app.route("/movies", methods=["POST"])
def add_movie():
    if not current_user:
        return jsonify({"error": "You must be logged in to add a movie"}), 401

    data = request.get_json()
    if not data or not all(
        key in data for key in ("name", "genre", "rating", "release_date")
    ):
        return jsonify({"error": "Missing required movie details"}), 400

        # Update movies.json file
    with open("./data/movies.json", "r+") as f:
        movies_data = json.load(f)
        new_movie = {
            "id": len(movies_data) + 1,
            **data,
        }
        movies_data.append(new_movie)
        f.seek(0)
        json.dump(movies_data, f, indent=4)

    return jsonify(new_movie), 201


if __name__ == "__main__":
    app.run(debug=True)
