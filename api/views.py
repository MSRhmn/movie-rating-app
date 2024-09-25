from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import User, Movie, Rating
from .serializers import (
    UserSerializer,
    MovieSerializer,
    RatingSerializer,
    LoginSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "message": "Login Successful"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to add movies.")
        serializer.save()


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RateMovieView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = RatingSerializer(
            {
                "user": request.user.id,
                "movie": movie.id,
                "rating": request.data.get("rating"),
            }
        )

        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(
                {"message": "Movie rated successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
