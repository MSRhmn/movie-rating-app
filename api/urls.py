from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MovieListView,
    MovieDetailView,
    RateMovieView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("movies/", MovieListView.as_view(), name="movies"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("movies/<int:movie_id>/rate/", RateMovieView.as_view(), name="rate_movie"),
]
