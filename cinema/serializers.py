from django.contrib.auth.models import User
from .models import Film
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('title', 'description', 'genre', 'premiere_date', 'session_time', 'film_duration', 'price')
