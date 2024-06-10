from django.contrib import admin

from apps.movie_management.models import Movie, Review, Genre

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)
