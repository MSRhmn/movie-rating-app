from flask import request, jsonify
import json
from app import app
from data import users, movies, ratings
from helpers import get_average_rating


current_user = None


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

    # Update 'movies.json' file
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


@app.route("/movies/<int:movie_id>/rate", methods=["POST"])
def rate_movie(movie_id):
    if not current_user:
        return jsonify({"error": "You must be logged in to rate a movie"}), 401

    data = request.get_json()
    if not data or not data.get("rating"):
        return jsonify({"error": "Missing rating value"}), 400

    rating = data["rating"]
    if not isinstance(rating, float) or rating < 0 or rating > 5:
        return jsonify({"error": "Invalid rating value"}), 400

    already_rated = any(
        rating["movie_id"] == movie_id and rating["user_id"] == current_user["id"]
        for rating in ratings
    )
    if already_rated:
        return jsonify({"error": "You already rated this movie"}), 400

    new_rating = {
        "id": len(ratings) + 1,
        "user_id": current_user["id"],
        "movie_id": movie_id,
        "rating": rating,
    }
    ratings.append(new_rating)

    # Update ratings.json file
    with open("ratings.json", "w") as f:
        json.dump(ratings, f, indent=4)

    return jsonify({"message": "Movie rated successfully"})
