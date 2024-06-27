from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name="api_user_set")
    user_permissions = models.ManyToManyField(Permission, related_name="api_user_set")


class Movie(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    release_date = models.DateField()

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movie_ratings"
    )
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}: {self.rating}"
