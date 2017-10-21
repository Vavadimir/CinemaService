from django.db import models


# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    genre = models.CharField(max_length=20)
    premiere_date = models.DateField()
    session_time = models.TimeField()
    film_duration = models.IntegerField()
    price = models.FloatField()


class Poster(models.Model):
    film = models.ForeignKey(Film)
    pic = models.ImageField(upload_to='static/images')
    is_main = models.BooleanField()


