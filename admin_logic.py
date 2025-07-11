from data.db import run_query
from services.movie_service import MovieService
from services.showtime_service import ShowtimeService

# admin_logic.py

def add_new_movie(title, description, showtimes, poster_url=None, trailer_url=None, price_per_seat=200):

    movie_id = MovieService.add_movie(title, description, poster_url, trailer_url, price_per_seat)
    for time in showtimes:
        ShowtimeService.add_showtime(movie_id, time)
    return movie_id


def remove_movie_by_id(movie_id):
    MovieService.delete_movie(movie_id)

def update_movie_showtime(movie_id, old_time, new_time):
    ShowtimeService.update_showtime(movie_id, old_time, new_time)

def add_movie_showtime(movie_id, time):
    ShowtimeService.add_showtime(movie_id, time)

def remove_movie_showtime(movie_id, time):
    ShowtimeService.remove_showtime(movie_id, time)

def list_movies():
    return MovieService.get_all_movies()

def list_showtime(movie_id):
    return ShowtimeService.get_showtimes_by_movie(movie_id)
