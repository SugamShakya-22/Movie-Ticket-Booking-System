from models.movie import Movie
from data.db import run_query

class MovieService:
    @staticmethod
    def get_all_movies():
        query = "SELECT id, title, description, poster_url FROM movies ORDER BY id DESC;"
        results = run_query(query, fetch=True)
        return [Movie(row["id"], row["title"], row["description"], row["poster_url"]) for row in results]

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

    @staticmethod
    def update_poster_url(movie_id, poster_url):
        query = "UPDATE movies SET poster_url = %s WHERE id = %s;"
        run_query(query, (poster_url, movie_id))

