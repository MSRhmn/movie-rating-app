from rest_framework import serializers

from .models import User, Movie, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "user", "movie", "rating", "created_at"]
