from db import run_query

def get_movies():
    query = "SELECT id, title, description FROM movies ORDER BY id;"
    return run_query(query, fetch=True)

def add_movie(title, description):
    query = "INSERT INTO movies (title, description) VALUES (%s, %s) RETURNING id;"
    result = run_query(query, (title, description), fetch=True)
    return result[0]["id"]

def delete_movie(movie_id):
    query = "DELETE FROM movies WHERE id = %s;"
    run_query(query, (movie_id,))
