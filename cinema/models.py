from django.db import models
from django.conf import settings


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

    def __str__(self):
        return str(self.pic)


class BookedPlace(models.Model):
    film = models.ForeignKey(Film, related_name="tickets")
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="customer",
        related_name="tickets",
    )
    place = models.IntegerField()
    row = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%d %d' % (self.row, self.place)