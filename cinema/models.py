from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe


class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    genre = models.CharField(max_length=20)
    premiere_date = models.DateField()
    session_time = models.TimeField()
    film_duration = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return str(self.id)

    def create(self, validated_data):
        return Poster.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.premiere_date = validated_data.get('premiere_date', instance.premiere_date)
        instance.session_time = validated_data.get('session_time', instance.session_time)
        instance.film_duration = validated_data.get('film_duration', instance.film_duration)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class Poster(models.Model):
    film = models.ForeignKey(Film)
    pic = models.ImageField(upload_to='images/')
    is_main = models.BooleanField(default=False)

    def create(self, validated_data):
        return Poster.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.film = validated_data.get('film', instance.film)
        instance.pic = validated_data.get('pic', instance.pic)
        instance.is_main = validated_data.get('is_main', instance.is_main)


class BookedPlace(models.Model):
    film = models.ForeignKey(Film)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="username",
    )
    place = models.IntegerField()
    row = models.IntegerField()

