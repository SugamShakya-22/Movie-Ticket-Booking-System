from models.booking import Booking
from data.db import run_query

class BookingService:
    @staticmethod
    def add_booking(user_id, showtime_id, seat_labels):
        booking_query = "INSERT INTO bookings (user_id, showtime_id) VALUES (%s, %s) RETURNING id;"
        result = run_query(booking_query, (user_id, showtime_id), fetch=True)
        booking_id = result[0]["id"]

        for seat in seat_labels:
            run_query("INSERT INTO booking_seats (booking_id, seat_label) VALUES (%s, %s);", (booking_id, seat))

        return booking_id

    @staticmethod
    def get_user_bookings(user_id):
        query = """
            SELECT 
                b.id AS booking_id,
                u.name AS user_name,
                m.title AS movie_title,
                s.time AS showtime
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN showtimes s ON b.showtime_id = s.id
            JOIN movies m ON s.movie_id = m.id
            WHERE b.user_id = %s
            ORDER BY b.id DESC;
        """
        results = run_query(query, (user_id,), fetch=True)

        bookings = []
        for row in results:
            seats_query = "SELECT seat_label FROM booking_seats WHERE booking_id = %s;"
            seats_result = run_query(seats_query, (row["booking_id"],), fetch=True)
            seat_list = [seat["seat_label"] for seat in seats_result]

            bookings.append({
                "booking_id": row["booking_id"],
                "user_name": row["user_name"],  # ✅ added
                "movie_title": row["movie_title"],
                "showtime": row["showtime"],
                "seats": seat_list
            })
        return bookings

    @staticmethod
    def get_booked_seats(movie_id, showtime_str):
        query = """
            SELECT bs.seat_label
            FROM booking_seats bs
            JOIN bookings b ON bs.booking_id = b.id
            JOIN showtimes s ON b.showtime_id = s.id
            WHERE s.movie_id = %s AND s.time = %s;
        """
        result = run_query(query, (movie_id, showtime_str), fetch=True)
        return [row["seat_label"] for row in result]

    @staticmethod
    def cancel_booking(booking_id):
        # Delete booking seats first due to foreign key constraints
        run_query("DELETE FROM booking_seats WHERE booking_id = %s;", (booking_id,))
        run_query("DELETE FROM bookings WHERE id = %s;", (booking_id,))

    @staticmethod
    def get_all_bookings():
        query = """
            SELECT b.id AS booking_id, u.name AS user_name, m.title AS movie_title, s.time AS showtime
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN showtimes s ON b.showtime_id = s.id
            JOIN movies m ON s.movie_id = m.id
            ORDER BY b.id DESC;
        """
        results = run_query(query, fetch=True)

        all_bookings = []
        for row in results:
            seats_query = "SELECT seat_label FROM booking_seats WHERE booking_id = %s;"
            seats_result = run_query(seats_query, (row["booking_id"],), fetch=True)
            seat_list = [seat["seat_label"] for seat in seats_result]

            all_bookings.append({
                "booking_id": row["booking_id"],
                "user_name": row["user_name"],
                "movie_title": row["movie_title"],
                "showtime": row["showtime"],
                "seats": seat_list
            })
        return all_bookings

    @staticmethod
    def get_booking_detail_by_id(booking_id):
        query = """
            SELECT b.id AS booking_id, u.name, m.title AS movie_title, s.time AS showtime
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN showtimes s ON b.showtime_id = s.id
            JOIN movies m ON s.movie_id = m.id
            WHERE b.id = %s;
        """
        result = run_query(query, (booking_id,), fetch=True)
        if not result:
            return None
        booking = result[0]

        seats_query = "SELECT seat_label FROM booking_seats WHERE booking_id = %s;"
        seats = run_query(seats_query, (booking_id,), fetch=True)
        booking["seats"] = [s["seat_label"] for s in seats]
        return booking

    @staticmethod
    def get_bookings_by_name(name):
        query = """
        SELECT b.id AS booking_id, m.title AS movie_title, s.time AS showtime
        FROM bookings b
        JOIN showtimes s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN users u ON b.user_id = u.id
        WHERE u.name ILIKE %s
        ORDER BY b.id DESC;
        """
        results = run_query(query, (f"%{name}%",), fetch=True)

        bookings = []
        for row in results:
            seats_query = "SELECT seat_label FROM booking_seats WHERE booking_id = %s;"
            seats_result = run_query(seats_query, (row["booking_id"],), fetch=True)
            seat_list = [seat["seat_label"] for seat in seats_result]

            bookings.append({
                "booking_id": row["booking_id"],
                "movie_title": row["movie_title"],
                "showtime": row["showtime"],
                "seats": seat_list
            })
        return bookings

    @staticmethod
    def get_booked_seats_by_showtime_id(showtime_id):
        query = """
                SELECT seat_label
                FROM booking_seats bs
                JOIN bookings b ON bs.booking_id = b.id
                WHERE b.showtime_id = %s;
            """
        result = run_query(query, (showtime_id,), fetch=True)
        return [row["seat_label"] for row in result]