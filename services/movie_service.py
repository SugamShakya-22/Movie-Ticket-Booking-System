from models.movie import Movie
from data.db import run_query

class MovieService:
    @staticmethod
    def get_all_movies():
        query = """
            SELECT id, title, description, poster_url, trailer_url, price_per_seat
            FROM movies ORDER BY id DESC;
        """
        results = run_query(query, fetch=True)
        return [
            Movie(
                row["id"], row["title"], row["description"],
                row.get("poster_url"), row.get("trailer_url"), row.get("price_per_seat")
            )
            for row in results
        ]

    @staticmethod
    def get_movie_by_id(movie_id):
        query = "SELECT * FROM movies WHERE id = %s;"
        result = run_query(query, (movie_id,), fetch=True)
        if result:
            row = result[0]
            return Movie(
                row["id"],
                row["title"],
                row["description"],
                row.get("poster_url"),
                row.get("trailer_url")  # include trailer_url if available
            )
        return None

    @staticmethod
    def add_movie(title, description, poster_url=None, trailer_url=None, price_per_seat=200):
        query = """
            INSERT INTO movies (title, description, poster_url, trailer_url, price_per_seat)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """
        result = run_query(query, (title, description, poster_url, trailer_url, price_per_seat), fetch=True)
        return result[0]["id"]

    @staticmethod
    def delete_movie(movie_id):
        query = "DELETE FROM movies WHERE id = %s;"
        run_query(query, (movie_id,))

    @staticmethod
    def update_poster_url(movie_id, poster_url):
        query = "UPDATE movies SET poster_url = %s WHERE id = %s;"
        run_query(query, (poster_url, movie_id))

    @staticmethod
    def update_trailer_url(movie_id, trailer_url):
        query = "UPDATE movies SET trailer_url = %s WHERE id = %s;"
        run_query(query, (trailer_url, movie_id))

    @staticmethod
    def update_price(movie_id, price):
        query = "UPDATE movies SET price_per_seat = %s WHERE id = %s;"
        run_query(query, (price, movie_id))


