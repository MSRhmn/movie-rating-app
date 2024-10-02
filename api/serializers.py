from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Movie, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            data["user"] = user
        else:
            raise serializers.ValidationError("Invalid credentials")
        return data


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "user", "movie", "rating", "created_at"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        # Create a new rating instance
        rating = Rating.objects.create(**validated_data)

        # Calculate and update the movie's average rating
        movie = validated_data['movie']
        average_rating = movie.average_rating()  # Get average rating from method

        # Update the movie's rating field (if you want to store it as average)
        if average_rating is not None:
            movie.rating = average_rating
            movie.save()

        return rating