import json
from datetime import datetime
import numpy as np

import requests
from apps.movie_management.models import Genre, Movie


def save_movie_list(page_number):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page_number}&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer api token"
    }

    response = requests.get(url, headers=headers)
    response1 = json.loads(response.text)

    for mov in response1.get('results'):
        release_date = datetime.strptime(mov['release_date'], "%Y-%m-%d").date()
        Movie.objects.create(id=mov['id'], title=mov['title'], description=mov['overview'],
                             release_date=release_date, genre_ids=mov['genre_ids'], poster=mov['poster_path'])

    return True


def save_genre():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer api token"
    }

    response = requests.get(url, headers=headers)
    response1 = json.loads(response.text)

    for gen in response1.get('genres'):
        Genre.objects.create(id=gen['id'], name=gen['name'])

    return True


class CollaborativeFiltering:
    def __init__(self, num_users, num_movies):
        self.num_users = num_users
        self.num_movies = num_movies
        self.user_movie_matrix = np.zeros((num_users, num_movies))

    def train(self, ratings):
        for rating in ratings:
            user_id, movie_id, rating_value = rating
            self.user_movie_matrix[user_id, movie_id] = rating_value

    def predict(self, user_id, movie_id):
        return self.user_movie_matrix[user_id, movie_id]

    def recommend_movies(self, user_id, top_n=10):
        user_ratings = self.user_movie_matrix[user_id]
        sorted_movie_indices = np.argsort(user_ratings)[::-1][:top_n]
        return sorted_movie_indices.tolist()
