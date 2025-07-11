from models.showtime import Showtime
from data.db import run_query

class ShowtimeService:
    @staticmethod
    def get_showtimes_by_movie(movie_id):
        query = "SELECT * FROM showtimes WHERE movie_id = %s ORDER BY time;"
        result = run_query(query, (movie_id,), fetch=True)
        return [Showtime(row["id"], row["movie_id"], row["time"]) for row in result]

    @staticmethod
    def add_showtime(movie_id, showtime_str):
        query = "INSERT INTO showtimes (movie_id, time) VALUES (%s, %s);"
        run_query(query, (movie_id, showtime_str))

    @staticmethod
    def remove_showtime(movie_id, showtime):
        query = "DELETE FROM showtimes WHERE movie_id = %s AND time = %s;"
        run_query(query, (movie_id, showtime.time))

    @staticmethod
    def update_showtime(movie_id, old_showtime_obj, new_time_str):
        query = "UPDATE showtimes SET time = %s WHERE movie_id = %s AND time = %s;"
        run_query(query, (new_time_str, movie_id, old_showtime_obj.time))

    @staticmethod
    def get_showtime_id(movie_id, time):
        query = "SELECT id FROM showtime WHERE movie_id = %s AND time = %s;"
        result = run_query(query, (movie_id, time), fetch=True)
        return result[0]["id"] if result else None

