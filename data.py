import json

# Load example data from JSON files.
with open("./data/users.json") as f:
    users = json.load(f)

with open("./data/movies.json") as f:
    movies = json.load(f)

with open("./data/ratings.json") as f:
    ratings = json.load(f)
