# pages/cancel_booking_page.py

import streamlit as st
from booking_logic import get_user_bookings, cancel_user_booking


class CancelBookingPage:
    def render(self):
        st.subheader("❌ Cancel Your Booking")

        name = st.text_input("Enter your name to find your bookings")

        if name:
            bookings = get_user_bookings(name)

            if not bookings:
                st.warning("No bookings found.")
            else:
                booking_options = [
                    f"ID {b['booking_id']}: {b['movie_title']} at {b['showtime']} (Seats: {', '.join(b.get('seats', []))})"
                    for b in bookings
                ]

                selected_booking = st.selectbox("Select a booking to cancel", booking_options)

                if st.button("Cancel Selected Booking"):
                    booking_id = int(selected_booking.split()[1].strip(":"))
                    cancel_user_booking(booking_id)
                    st.success(f"Booking ID {booking_id} has been canceled.")
                    st.experimental_rerun()
