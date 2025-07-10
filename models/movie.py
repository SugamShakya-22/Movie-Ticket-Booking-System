# models/movie.py
class Movie:
    def __init__(self, movie_id, title, description, poster_url=None):
        self.movie_id = movie_id
        self.title = title
        self.description = description
        self.poster_url = poster_url


    def __str__(self):
        return f"{self.title} - {self.description}"
