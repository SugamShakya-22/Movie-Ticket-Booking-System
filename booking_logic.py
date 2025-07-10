# booking_logic.py
from services.booking_service import BookingService
from data.showtime import get_showtime_id
from services.showtime_service import ShowtimeService
from data.movies import get_movies


def confirm_booking(user_id, movie_id, showtime, seat_list):
    # Get showtime id for the movie and showtime string
    showtime_id = get_showtime_id(movie_id, showtime)
    if showtime_id is None:
        raise ValueError("Showtime not found")

    return BookingService.add_booking(user_id, showtime_id, seat_list)


def get_available_seats(movie_id, showtime_time):
    all_seats = [row + str(col) for row in ['A', 'B', 'C', 'D', 'E'] for col in range(1, 7)]
    booked_seats = BookingService.get_booked_seats(movie_id, showtime_time)
    return [seat for seat in all_seats if seat not in booked_seats]


def get_user_bookings(user_id):
    return BookingService.get_user_bookings(user_id)


def cancel_user_booking(booking_id):
    BookingService.cancel_booking(booking_id)


def get_all_bookings():
    return BookingService.get_all_bookings()


def get_booking_details(booking_id):
    return BookingService.get_booking_detail_by_id(booking_id)


def get_bookings_by_name(name):
    return BookingService.get_bookings_by_name(name)

def get_booked_seats(movie_id, showtime_str):
    # Get showtime_id first via ShowtimeService
    showtimes = ShowtimeService.get_showtimes_by_movie(movie_id)
    showtime_id = None
    for st in showtimes:
        if st.time == showtime_str:
            showtime_id = st.showtime_id
            break
    if showtime_id is None:
        return []

    # Now use BookingService to find booked seats for that showtime_id
    return BookingService.get_booked_seats_by_showtime_id(showtime_id)
