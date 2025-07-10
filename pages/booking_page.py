import streamlit as st
from services.movie_service import MovieService
from services.showtime_service import ShowtimeService
from services.booking_service import BookingService

class BookingPage:
    def render(self):
        st.subheader("🎟️ Book Tickets")

        if not st.session_state.get("user"):
            st.warning("Please login to book tickets.")
            return

        user_id = st.session_state.user["id"]

        movies = MovieService.get_all_movies()
        if not movies:
            st.warning("No movies available for booking.")
            return

        movie_titles = [m.title for m in movies]
        selected_movie_title = st.selectbox("Select Movie", movie_titles)
        movie = next((m for m in movies if m.title == selected_movie_title), None)
        movie_id = movie.movie_id

        showtimes = ShowtimeService.get_showtimes_by_movie(movie_id)
        if not showtimes:
            st.warning("No showtimes available for the selected movie.")
            return

        showtime_options = [s.time for s in showtimes]
        selected_showtime = st.selectbox("Select Showtime", showtime_options)

        num_seats = st.number_input("How many seats?", min_value=1, max_value=5, value=1, step=1)

        booked_seats = BookingService.get_booked_seats(movie_id, selected_showtime)
        all_seats = [row + str(col) for row in ['A', 'B', 'C', 'D', 'E'] for col in range(1, 7)]
        available_seats = [seat for seat in all_seats if seat not in booked_seats]

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
                        st.rerun()
                else:
                    if col.button(f"🟤 {seat}", key=f"available_{seat}"):
                        if len(selected_seats) < num_seats:
                            selected_seats.add(seat)
                            st.rerun()

        st.session_state.selected_seats = selected_seats

        if st.button("Confirm Booking"):
            if len(selected_seats) != num_seats:
                st.warning("Please select the required number of seats.")
            else:
                showtime_obj = next((s for s in showtimes if s.time == selected_showtime), None)
                if showtime_obj is None:
                    st.error("Invalid showtime selected.")
                    return

                BookingService.add_booking(user_id=user_id, showtime_id=showtime_obj.showtime_id, seat_labels=list(selected_seats))
                st.success("✅ Booking confirmed!")
                st.session_state.selected_seats = set()
                st.button("Refresh", on_click= st.rerun)
