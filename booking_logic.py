# booking_logic.py
from data.bookings import add_booking, get_booked_seats, get_bookings_by_name, cancel_booking, get_all_booking_records, get_booking_detail_by_id
from data.showtime import get_showtime_id
from data.movies import get_movies

def confirm_booking(user_id, name, movie_id, showtime, seat_list):
    showtime_id = get_showtime_id(movie_id, showtime)
    return add_booking(user_id, name, showtime_id, seat_list)

def get_available_seats(movie_id, showtime_time):
    all_seats = [row + str(col) for row in ['A', 'B', 'C', 'D', 'E'] for col in range(1, 7)]
    booked_seats = get_booked_seats(movie_id, showtime_time)
    return [seat for seat in all_seats if seat not in booked_seats]

def get_user_bookings(name):
    return get_bookings_by_name(name)

def cancel_user_booking(booking_id):
    cancel_booking(booking_id)

def get_all_bookings():
    return get_all_booking_records()

def get_booking_details(booking_id):
    booking = get_booking_detail_by_id(booking_id)
    if not booking:
        return None
    seats = get_booking_seats_by_booking_id(booking_id)
    booking['seats'] = seats
    return booking
