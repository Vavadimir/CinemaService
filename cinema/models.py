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


class Poster(models.Model):
    film = models.ForeignKey(Film)
    pic = models.ImageField(upload_to='images/')
    is_main = models.BooleanField(default=False)


class BookedPlace(models.Model):
    film = models.ForeignKey(Film)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="username",
    )
    place = models.IntegerField()
    row = models.IntegerField()

