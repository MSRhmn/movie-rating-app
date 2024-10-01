from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


def validate_rating(value):
    if value < 0 or value > 10:
        raise ValidationError("Rating must be between 0 and 10.")


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[validate_rating]
    )
    release_date = models.DateField()

    def average_rating(self):
        ratings = self.movie_ratings.all()
        if ratings.exists():
            return ratings.aggregate(models.Avg("rating"))["rating__avg"]
        return None

    def __str__(self):
        return f"{self.title} ({self.release_date.year})"

    class Meta:
        ordering = ["release_date"]


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movie_ratings"
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[validate_rating]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.rating}"

    class Meta:
        unique_together = ("user", "movie")
