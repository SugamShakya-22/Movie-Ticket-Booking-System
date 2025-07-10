# pages/booking_page.py

import streamlit as st
from booking_logic import confirm_booking, get_all_movies, \
    get_movie_id_by_title, get_showtime, get_available_seats


class BookingPage:
    def render(self):
        st.subheader("🎟️ Book Tickets")

        movies = get_all_movies()
        movie_titles = [m["title"] for m in movies]

        if not movie_titles:
            st.warning("No movies available for booking.")
            return

        selected_movie_title = st.selectbox("Select Movie", movie_titles)
        movie_id = get_movie_id_by_title(selected_movie_title)

        showtimes = get_showtime(movie_id)
        selected_showtime = st.selectbox("Select Showtime", showtimes)

        num_seats = st.number_input("How many seats?", min_value=1, max_value=5, value=1, step=1)
        name = st.text_input("Your Name")

        booked_seats = get_available_seats(movie_id, selected_showtime)
        all_seats = [row + str(col) for row in ['A', 'B', 'C', 'D', 'E'] for col in range(1, 7)]

        if "selected_seats" not in st.session_state:
            st.session_state.selected_seats = set()

        selected_seats = st.session_state.selected_seats

        st.markdown("### 🪑 Select Your Seats")

        for row in ['A', 'B', 'C', 'D', 'E']:
            cols = st.columns(6)
            for i, col in enumerate(cols):
                seat = row + str(i + 1)

                if seat in booked_seats:
                    col.button(f"🔴 {seat}", disabled=True, key=f"booked_{seat}")
                elif seat in selected_seats:
                    if col.button(f"🟢 {seat}", key=f"selected_{seat}"):
                        selected_seats.remove(seat)
                else:
                    if col.button(f"🟤 {seat}", key=f"available_{seat}"):
                        if len(selected_seats) < num_seats:
                            selected_seats.add(seat)

        st.session_state.selected_seats = selected_seats

        if st.button("Confirm Booking"):
            if name.strip() == "" or len(selected_seats) != num_seats:
                st.warning("Please enter name and select required number of seats.")
            else:
                confirm_booking(name, movie_id, selected_showtime, list(selected_seats))
                st.success("✅ Booking confirmed!")
                st.session_state.selected_seats = set()
                st.experimental_rerun()
