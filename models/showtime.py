class Showtime:
    def __init__(self, showtime_id, movie_id, showtime_str):
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.time = showtime_str

    def __str__(self):
        return self.time
