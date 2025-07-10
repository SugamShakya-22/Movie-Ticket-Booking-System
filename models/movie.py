# models/movie.py
class Movie:
    def __init__(self, movie_id, title, description, poster_url=None, trailer_url=None, price_per_seat=0.0):
        self.movie_id = movie_id
        self.title = title
        self.description = description
        self.poster_url = poster_url
        self.trailer_url = trailer_url
        self.price_per_seat = price_per_seat


    def __str__(self):
        return f"{self.title} - {self.description}"
