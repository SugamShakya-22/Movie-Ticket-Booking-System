from models.booking import Booking
from data import run_query

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
        SELECT b.id AS booking_id, s.showtime, m.title AS movie_title
        FROM bookings b
        JOIN showtimes s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        WHERE b.user_id = %s
        ORDER BY b.id DESC;
        """
        return run_query(query, (user_id,), fetch=True)
