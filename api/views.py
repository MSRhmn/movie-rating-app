from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import User, Movie, Rating
from .serializers import UserSerializer, MovieSerializer, RatingSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=400)


class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class RateMovieView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, movie_id):
        rating_value = request.data.get("rating")
        movie = Movie.objects.get(id=movie_id)
        rating = Rating.objects.create(
            user=request.user, movie=movie, rating=rating_value
        )
        return Response({"message": "Movie rated successfully"})
