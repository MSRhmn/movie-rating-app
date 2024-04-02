from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load example data from JSON files.
with open("./data/users.json") as f:
    users = json.load(f)

with open("./data/movies.json") as f:
    movies = json.load(f)

with open("./data/ratings.json") as f:
    ratings = json.load(f)

current_user = None

# Define a helper function to calculate average rating for a movie.
def get_average_rating(movie_id):
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


if __name__ == "__main__":
    app.run(debug=True)
