from models.movie import Movie
from data import run_query

class MovieService:
    @staticmethod
    def get_all_movies():
        query = "SELECT * FROM movies ORDER BY id;"
        result = run_query(query, fetch=True)
        return [Movie(row["id"], row["title"], row["description"]) for row in result]

    @staticmethod
    def get_movie_by_id(movie_id):
        query = "SELECT * FROM movies WHERE id = %s;"
        result = run_query(query, (movie_id,), fetch=True)
        if result:
            row = result[0]
            return Movie(row["id"], row["title"], row["description"])
        return None

    @staticmethod
    def add_movie(title, description):
        query = "INSERT INTO movies (title, description) VALUES (%s, %s) RETURNING id;"
        result = run_query(query, (title, description), fetch=True)
        return result[0]["id"]

    @staticmethod
    def delete_movie(movie_id):
        query = "DELETE FROM movies WHERE id = %s;"
        run_query(query, (movie_id,))
