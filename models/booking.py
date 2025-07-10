class Booking:
    def __init__(self, booking_id, user_id, showtime_id, seat_list):
        self.booking_id = booking_id
        self.user_id = user_id
        self.showtime_id = showtime_id
        self.seat_list = seat_list

    def __str__(self):
        return f"Booking #{self.booking_id} for seats: {', '.join(self.seat_list)}"
