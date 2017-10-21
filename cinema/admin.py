from django.contrib import admin
from .models import Film


class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'genre', 'premiere_date', 'session_time', 'film_duration', 'price')


admin.site.register(Film, FilmAdmin)