from data import ratings


def get_average_rating(movie_id):
    """Define a helper function to calculate average rating for a movie."""
    movie_ratings = [rating for rating in ratings if rating["movie_id"] == movie_id]
    if movie_ratings:
        return sum(rating["rating"] for rating in movie_ratings) / len(movie_ratings)
    else:
        return f"There is no ratings yet for movie id: `{movie_id}`."
