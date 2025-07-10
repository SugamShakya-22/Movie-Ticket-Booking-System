from models.showtime import Showtime
from data import run_query

class ShowtimeService:
    @staticmethod
    def get_showtimes_by_movie(movie_id):
        query = "SELECT * FROM showtimes WHERE movie_id = %s ORDER BY showtime;"
        result = run_query(query, (movie_id,), fetch=True)
        return [Showtime(row["id"], row["movie_id"], row["showtime"]) for row in result]

    @staticmethod
    def add_showtime(movie_id, showtime_str):
        query = "INSERT INTO showtimes (movie_id, showtime) VALUES (%s, %s);"
        run_query(query, (movie_id, showtime_str))

    @staticmethod
    def remove_showtime(movie_id, showtime_str):
        query = "DELETE FROM showtimes WHERE movie_id = %s AND showtime = %s;"
        run_query(query, (movie_id, showtime_str))

    @staticmethod
    def update_showtime(movie_id, old_time, new_time):
        query = "UPDATE showtimes SET showtime = %s WHERE movie_id = %s AND showtime = %s;"
        run_query(query, (new_time, movie_id, old_time))
