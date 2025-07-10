from db import run_query

def add_showtime(movie_id, time):
    query = "INSERT INTO showtime (movie_id, time) VALUES (%s, %s);"
    run_query(query, (movie_id, time))

def get_showtime_for_movie(movie_id):
    query = "SELECT time FROM showtime WHERE movie_id = %s ORDER BY id;"
    result = run_query(query, (movie_id,), fetch=True)
    return [row['time'] for row in result]

def remove_showtime(movie_id, time):
    query = "DELETE FROM showtime WHERE movie_id = %s AND time = %s;"
    run_query(query, (movie_id, time))

def update_showtime(movie_id, old_time, new_time):
    query = "UPDATE showtime SET time = %s WHERE movie_id = %s AND time = %s;"
    run_query(query, (new_time, movie_id, old_time))

def get_showtime_id(movie_id, time):
    query = "SELECT id FROM showtime WHERE movie_id = %s AND time = %s;"
    result = run_query(query, (movie_id, time), fetch=True)
    return result[0]["id"] if result else None
