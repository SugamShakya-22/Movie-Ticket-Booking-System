# page/admin_panel.py

import streamlit as st

from admin_logic import (
    remove_movie_by_id,
    add_movie_showtime, remove_movie_showtime,
    update_movie_showtime, list_movies, list_showtime
)
from booking_logic import (
    get_booking_details, get_booked_seats, get_available_seats
)
from services.booking_service import BookingService
from services.movie_service import MovieService
from services.showtime_service import ShowtimeService


class AdminPanel:
    def render(self):
        st.subheader("👤 Admin Panel")

        admin_action = st.selectbox("Action", [
            "Add Movie", "Update Ticket Price", "Update Movie Trailer", "Update Movie Poster", "Remove Movie", "Update Showtimes",
            "View Movies", "View Bookings", "View Seats Status",
            "View Showtimes", "View Booking Details", "View Booking History"
        ])

        movies = list_movies()

        if admin_action == "Add Movie":
            title = st.text_input("Movie Title")
            description = st.text_area("Description")
            showtimes_str = st.text_input("Showtimes (comma separated)")

            poster_url = st.text_input("Poster Image URL (optional)")
            trailer_url = st.text_input("Trailer URL (YouTube iframe or direct link)")
            price_per_seat = st.number_input("Price per Seat", min_value=0.0, value=200.0, step=10.0)

            if st.button("Add Movie"):
                if not title or not description:
                    st.warning("Title and description are required.")
                else:
                    showtimes = [s.strip() for s in showtimes_str.split(",")]
                    movie_id = MovieService.add_movie(
                        title=title,
                        description=description,
                        showtimes=showtimes,
                        poster_url=poster_url.strip() or None,
                        trailer_url=trailer_url.strip() or None,
                        price_per_seat=price_per_seat
                    )
                    st.success(f"✅ Movie '{title}' added successfully!")

        elif admin_action == "Update Ticket Price":
            movies = MovieService.get_all_movies()
            if movies:
                selected_movie = st.selectbox("Select Movie", movies, format_func=lambda m: m.title)
                new_price = st.number_input("New Price per Seat", min_value=0.0,
                                            value=selected_movie.price_per_seat or 0.0, step=10.0)
                if st.button("Update Price"):
                    MovieService.update_price(selected_movie.movie_id, new_price)
                    st.success("✅ Price updated successfully.")
            else:
                st.info("No movies available.")

        elif admin_action == "Update Movie Trailer":
            movies = MovieService.get_all_movies()
            if not movies:
                st.info("No movies available.")
                return

            selected_movie = st.selectbox(
                "Select Movie to Update Trailer",
                movies,
                format_func=lambda m: m.title
            )

            new_trailer_url = st.text_input("New Trailer URL")

            if st.button("Update Trailer"):
                if new_trailer_url.strip():
                    MovieService.update_trailer_url(selected_movie.movie_id, new_trailer_url.strip())
                    st.success(f"Trailer for '{selected_movie.title}' updated successfully!")
                else:
                    st.warning("Please enter a valid trailer URL.")

        elif admin_action == "Update Movie Poster":
            movies = MovieService.get_all_movies()
            if not movies:
                st.warning("No movies found.")
                return

            movie = st.selectbox("🎞️ Select Movie to Update Poster", movies, format_func=lambda m: m.title)
            new_url = st.text_input("🖼️ New Poster URL")

            if st.button("Update Poster"):
                if new_url.strip():
                    MovieService.update_poster_url(movie.movie_id, new_url.strip())
                    st.success(f"Poster for '{movie.title}' updated successfully!")
                else:
                    st.warning("Please enter a valid image URL.")


        elif admin_action == "Remove Movie":
            if not movies:
                st.info("No movies to remove.")
            else:
                movie_options = [f"ID {m.movie_id}: {m.title}" for m in movies]
                selected = st.selectbox("Select a movie to remove", movie_options)
                movie_id = int(selected.split()[1].strip(":"))

                if st.button("Remove Movie"):
                    remove_movie_by_id(movie_id)
                    st.success(f"Movie ID {movie_id} has been removed.")
                    st.button("Refresh", st.rerun)

        elif admin_action == "Update Showtimes":
            if not movies:
                st.info("No movies available.")
            else:
                movie_options = [f"ID {m.movie_id}: {m.title}" for m in movies]
                selected = st.selectbox("Select a movie", movie_options)
                movie_id = int(selected.split()[1].strip(":"))
                showtimes = list_showtime(movie_id)

                st.markdown("#### Existing Showtimes")
                if not showtimes:
                    st.write("No showtimes found.")
                else:
                    selected_showtime = st.selectbox("Select showtime to remove", showtimes)
                    if st.button("Remove Showtime"):
                        remove_movie_showtime(movie_id, selected_showtime)
                        st.success(f"Removed showtime: {selected_showtime}")
                        st.button("Refresh", st.rerun)

                st.markdown("#### Add New Showtime")
                new_showtime = st.text_input("Enter new showtime (e.g., 3:00 PM)")
                if st.button("Add Showtime"):
                    if new_showtime.strip() == "":
                        st.warning("Please enter a showtime.")
                    else:
                        add_movie_showtime(movie_id, new_showtime.strip())
                        st.success(f"Added new showtime: {new_showtime}")
                        st.button("Refresh", st.rerun)

                st.markdown("#### Edit Existing Showtime")
                if showtimes:
                    selected_time_to_edit = st.selectbox("Select showtime to edit", showtimes, key="edit_time_select")
                    new_time = st.text_input("Enter new showtime", key="new_time_input")
                    if st.button("Update Showtime"):
                        if new_time.strip() == "":
                            st.warning("Please enter a new showtime.")
                        else:
                            update_movie_showtime(movie_id, selected_time_to_edit, new_time.strip())
                            st.success(f"Updated showtime from '{selected_time_to_edit}' to '{new_time.strip()}'")
                            st.button("Refresh", st.rerun)

        elif admin_action == "View Movies":
            st.subheader("🎬 All Movies")
            if not movies:
                st.info("No movies found.")
            else:
                for movie in movies:
                    st.markdown(f"**{movie.title}** (ID: {movie.movie_id})")
                    st.caption(movie.description)
                    showtimes = list_showtime(movie.movie_id)
                    st.write("Showtimes:", ", ".join([s.time for s in showtimes]) if showtimes else "No showtimes available.")

                    st.markdown("---")

        elif admin_action == "View Bookings":
            st.subheader("📋 All Bookings")
            bookings = BookingService.get_all_bookings()
            if bookings:
                for booking in bookings:
                    st.markdown(f"""
                            **Booking ID:** {booking['booking_id']}  
                            **User:** {booking['user_name']}  
                            **Movie:** {booking['movie_title']}  
                            **Showtime:** {booking['showtime']}  
                            **Seats:** {', '.join(booking['seats'])}  
                            **💰 Total Price:** Rs. {booking['total_price']}  
                        """)
                    st.markdown("---")
            else:
                st.info("No bookings available.")

        elif admin_action == "View Seats Status":
            st.subheader("🪑 View Seats Status")
            if not movies:
                st.info("No movies available.")
            else:
                selected_movie = st.selectbox("Select Movie", [f"{m.title} (ID: {m.movie_id})" for m in movies])
                movie_id = int(selected_movie.split("ID: ")[1].rstrip(")"))
                showtimes = list_showtime(movie_id)
                if not showtimes:
                    st.info("No showtimes for this movie.")
                else:
                    selected_showtime = st.selectbox("Select Showtime", showtimes)
                    booked_seats = get_booked_seats(movie_id, selected_showtime.time)
                    available_seats = get_available_seats(movie_id, selected_showtime.time)
                    st.write("Booked Seats:", ", ".join(booked_seats) if booked_seats else "No seats booked.")
                    st.write("Available Seats:", ", ".join(available_seats) if available_seats else "No seats available.")

        elif admin_action == "View Showtimes":
            st.subheader("⏰ All Showtimes")
            if not movies:
                st.info("No movies available.")
            else:
                for movie in movies:
                    showtimes = ShowtimeService.get_showtimes_by_movie(movie.movie_id)
                    showtime_strs = [s.time for s in showtimes]
                    st.markdown(f"**{movie.title}**: {', '.join(showtime_strs) if showtime_strs else 'No showtimes'}")


        elif admin_action == "View Booking Details":
            st.subheader("🔎 Booking Details")
            booking_id = st.number_input("Enter Booking ID", min_value=1, step=1)
            if st.button("Fetch Details"):
                details = get_booking_details(booking_id)
                if not details:
                    st.warning("Booking not found.")
                else:
                    st.write(details)

        elif admin_action == "View Booking History":
            st.subheader("📜 Booking History by User ID")
            user_id = st.text_input("Enter User ID to view bookings")

            if user_id:
                try:
                    user_id_int = int(user_id)
                    bookings = BookingService.get_user_bookings(user_id_int)
                    if bookings:
                        for booking in bookings:
                            st.write(f"Booking ID: {booking['booking_id']}")
                            st.write(f"User: {booking['user_name']}")
                            st.write(f"Movie: {booking['movie_title']}")
                            st.write(f"Showtime: {booking['showtime']}")
                            st.write(f"Seats: {', '.join(booking['seats'])}")
                            st.write("---")
                    else:
                        st.info("No bookings found for this user.")
                except ValueError:
                    st.error("Please enter a valid numeric user ID.")
