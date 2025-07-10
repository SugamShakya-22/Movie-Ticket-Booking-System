import streamlit as st
from services.movie_service import MovieService
from services.showtime_service import ShowtimeService
from services.booking_service import BookingService

class BookingPage:
    def render(self):
        st.subheader("🎟️ Book Tickets")

        movies = MovieService.get_all_movies()
        if not movies:
            st.warning("No movies available for booking.")
            return

        # Movie and Showtime Selection
        selected_movie = st.selectbox("Select Movie", movies, format_func=lambda m: m.title)
        movie_id = selected_movie.movie_id
        price_per_seat = selected_movie.price_per_seat or 0.0

        showtimes = ShowtimeService.get_showtimes_by_movie(movie_id)
        if not showtimes:
            st.info("No showtimes available for this movie.")
            return

        selected_showtime = st.selectbox("Select Showtime", [s.time for s in showtimes])

        # Seat Selection
        num_seats = st.number_input("How many seats?", min_value=1, max_value=5, value=1, step=1)
        booked_seats = BookingService.get_booked_seats(movie_id, selected_showtime)
        all_seats = [row + str(col) for row in 'ABCDE' for col in range(1, 7)]
        available_seats = [seat for seat in all_seats if seat not in booked_seats]

        if "selected_seats" not in st.session_state:
            st.session_state.selected_seats = set()
        selected_seats = st.session_state.selected_seats

        st.markdown("### 🪑 Select Your Seats")
        for row in 'ABCDE':
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

        # 💰 Show Price Calculation
        if len(selected_seats) == num_seats:
            total_price = price_per_seat * num_seats
            st.info(f"💰 Total Price: Rs. {price_per_seat} x {num_seats} = Rs. {total_price}")

        # Confirm Booking
        if st.button("Confirm Booking"):
            if len(selected_seats) != num_seats:
                st.warning("Please select the required number of seats.")
            else:
                showtime_obj = next((s for s in showtimes if s.time == selected_showtime), None)
                user_id = st.session_state.user["id"]
                BookingService.add_booking(user_id=user_id, showtime_id=showtime_obj.showtime_id,
                                           seat_labels=list(selected_seats))

                st.success("✅ Booking confirmed!")
                st.session_state.selected_seats = set()
                st.button("Refresh", on_click=st.rerun)
