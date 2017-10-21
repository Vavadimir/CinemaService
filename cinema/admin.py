from django.contrib import admin
from .models import Film, Poster


class FilmAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'genre', 'premiere_date', 'session_time', 'film_duration', 'price')


class PosterAdmin(admin.ModelAdmin):
    list_display = ('film', 'pic')


admin.site.register(Film, FilmAdmin)
admin.site.register(Poster, PosterAdmin)