import streamlit as st
from services.booking_service import BookingService

class CancelBookingPage:
    def render(self):
        st.subheader("❌ Cancel Booking")

        # Check if user is logged in
        if not st.session_state.get("user"):
            st.warning("Please login to view and cancel your bookings.")
            return

        user = st.session_state.user
        user_id = st.session_state.user["id"]

        user_name = user["name"]

        st.write(f"Showing bookings for: **{user_name}**")

        # Fetch bookings for logged-in user
        bookings = BookingService.get_user_bookings(user_id)
        if not bookings:
            st.info("You have no bookings to cancel.")
            return

        # Display bookings with cancel button
        for booking in bookings:
            booking_id = booking["booking_id"]
            movie_title = booking["movie_title"]
            showtime = booking["showtime"]
            seats = ", ".join(booking["seats"])

            st.markdown(f"**Booking ID:** {booking_id}")
            st.markdown(f"**Movie:** {movie_title}")
            st.markdown(f"**Showtime:** {showtime}")
            st.markdown(f"**Seats:** {seats}")


            if st.button(f"Cancel Booking {booking_id}", key=f"cancel_{booking_id}"):
                BookingService.cancel_booking(booking_id)
                st.success(f"Booking {booking_id} cancelled successfully!")
