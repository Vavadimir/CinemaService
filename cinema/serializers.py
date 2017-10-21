from django.contrib.auth.models import User
from .models import Film, Poster
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('id', 'title', 'description', 'genre', 'premiere_date', 'session_time', 'film_duration', 'price')


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = ('film', 'pic', 'is_main')