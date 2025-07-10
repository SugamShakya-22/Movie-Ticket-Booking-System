# data.py
from data.db import run_query
# Initial movie list (in-memory storage)

def get_movies():
    query = "SELECT id, title, description FROM movies ORDER BY id;"
    return run_query(query, fetch=True)

def add_movie(title, description):
    query = "INSERT INTO movies (title, description) VALUES (%s, %s) RETURNING id;"
    result = run_query(query, (title, description), fetch=True)
    return result[0]["id"]

def add_showtime(movie_id, time):
    query = "INSERT INTO showtime (movie_id, time) VALUES (%s, %s);"
    run_query(query, (movie_id, time))

def get_showtime_for_movie(movie_id):
    query = "SELECT time FROM showtime WHERE movie_id = %s ORDER BY id;"
    result = run_query(query, (movie_id,), fetch=True)
    return [row['time'] for row in result]

def delete_movie(movie_id):
    query = "DELETE FROM movies WHERE id = %s;"
    run_query(query, (movie_id,))

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

def add_booking(user_id, name, showtime_id, seat_labels):
    query = """
        INSERT INTO bookings (user_id, name, showtime_id)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    result = run_query(query, (user_id, name, showtime_id), fetch=True)
    booking_id = result[0]["id"]

    # Insert seat labels
    seat_query = "INSERT INTO booking_seats (booking_id, seat_label) VALUES (%s, %s);"
    for seat in seat_labels:
        run_query(seat_query, (booking_id, seat))

    return booking_id


def get_booked_seats(movie_id, showtime_time):
    query = """
    SELECT bs.seat_label
    FROM booking_seats bs
    JOIN bookings b ON bs.booking_id = b.id
    JOIN showtime s ON b.showtime_id = s.id
    WHERE s.movie_id = %s AND s.time = %s;
    """
    results = run_query(query, (movie_id, showtime_time), fetch=True)
    return [r["seat_label"] for r in results]

def get_bookings_by_name(name):
    query = """
        SELECT b.id AS booking_id, m.title AS movie_title, s.time AS showtime
        FROM bookings b
        JOIN showtime s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        WHERE b.name ILIKE %s
        ORDER BY b.id DESC;
    """
    return run_query(query, (f"%{name}%",), fetch=True)

def cancel_booking(booking_id):
    query = "DELETE FROM bookings WHERE id = %s;"
    run_query(query, (booking_id,))

def get_all_booking_records():
    query = """
        SELECT b.id AS booking_id, b.name, m.title AS movie_title, s.time AS showtime
        FROM bookings b
        JOIN showtime s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        ORDER BY b.id DESC;
    """
    return run_query(query, fetch=True)

def get_booking_seats_by_booking_id(booking_id):
    query = "SELECT seat_label FROM booking_seats WHERE booking_id = %s;"
    results = run_query(query, (booking_id,), fetch=True)
    return [r["seat_label"] for r in results]

def get_booking_detail_by_id(booking_id):
    query = """
        SELECT b.id AS booking_id, b.name, m.title AS movie_title, s.time AS showtime
        FROM bookings b
        JOIN showtime s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        WHERE b.id = %s;
    """
    result = run_query(query, (booking_id,), fetch=True)
    return result[0] if result else None

