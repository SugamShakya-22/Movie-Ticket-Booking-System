# pages/admin_panel.py

import streamlit as st
from admin_logic import add_movie, remove_movie
from data.data import get_movies, get_showtime_for_movie, remove_showtime, add_showtime, update_showtime
from booking_logic import get_all_bookings, get_user_bookings, get_booking_details, get_booked_seats, get_available_seats


class AdminPanel:
    def render(self):
        st.subheader("👤 Admin Panel")

        admin_action = st.selectbox("Action", [
            "Add Movie", "Remove Movie", "Update Showtimes", "View Movies", "View Bookings",
            "View Seats Status", "View Showtimes", "View Booking Details", "View Booking History"
        ])

        movies = get_movies()

        if admin_action == "Add Movie":
            title = st.text_input("Movie Title")
            description = st.text_area("Description")
            showtimes_str = st.text_input("Showtimes (comma separated)")

            if st.button("Add Movie"):
                if title.strip() == "" or showtimes_str.strip() == "":
                    st.warning("Please fill all fields.")
                else:
                    showtimes = [s.strip() for s in showtimes_str.split(",")]
                    movie_id = add_movie(title, description, showtimes)
                    st.success(f"Movie '{title}' added with ID {movie_id}.")

        elif admin_action == "Remove Movie":
            if not movies:
                st.info("No movies to remove.")
            else:
                movie_options = [f"ID {m['id']}: {m['title']}" for m in movies]
                selected = st.selectbox("Select a movie to remove", movie_options)
                movie_id = int(selected.split()[1].strip(":"))

                if st.button("Remove Movie"):
                    remove_movie(movie_id)
                    st.success(f"Movie ID {movie_id} has been removed.")
                    st.experimental_rerun()

        elif admin_action == "Update Showtimes":
            if not movies:
                st.info("No movies available.")
            else:
                movie_options = [f"ID {m['id']}: {m['title']}" for m in movies]
                selected = st.selectbox("Select a movie", movie_options)
                movie_id = int(selected.split()[1].strip(":"))
                showtimes = get_showtime_for_movie(movie_id)

                st.markdown("#### Existing Showtimes")
                if not showtimes:
                    st.write("No showtimes found.")
                else:
                    selected_showtime = st.selectbox("Select showtime to remove", showtimes)
                    if st.button("Remove Showtime"):
                        remove_showtime(movie_id, selected_showtime)
                        st.success(f"Removed showtime: {selected_showtime}")
                        st.experimental_rerun()

                st.markdown("#### Add New Showtime")
                new_showtime = st.text_input("Enter new showtime (e.g., 3:00 PM)")
                if st.button("Add Showtime"):
                    if new_showtime.strip() == "":
                        st.warning("Please enter a showtime.")
                    else:
                        add_showtime(movie_id, new_showtime.strip())
                        st.success(f"Added new showtime: {new_showtime}")
                        st.experimental_rerun()

                st.markdown("#### Edit Existing Showtime")
                if showtimes:
                    selected_time_to_edit = st.selectbox("Select showtime to edit", showtimes, key="edit_time_select")
                    new_time = st.text_input("Enter new showtime", key="new_time_input")
                    if st.button("Update Showtime"):
                        if new_time.strip() == "":
                            st.warning("Please enter a new showtime.")
                        else:
                            update_showtime(movie_id, selected_time_to_edit, new_time.strip())
                            st.success(f"Updated showtime from '{selected_time_to_edit}' to '{new_time.strip()}'")
                            st.experimental_rerun()

        elif admin_action == "View Movies":
            st.subheader("🎬 All Movies")
            if not movies:
                st.info("No movies found.")
            else:
                for movie in movies:
                    st.markdown(f"**{movie['title']}** (ID: {movie['id']})")
                    st.caption(movie['description'])
                    showtimes = get_showtime_for_movie(movie["id"])
                    st.write("Showtimes:", ", ".join(showtimes) if showtimes else "No showtimes available.")
                    st.markdown("---")

        elif admin_action == "View Bookings":
            st.subheader("📋 All Bookings")
            bookings = get_all_bookings()
            if not bookings:
                st.info("No bookings found.")
            else:
                for b in bookings:
                    st.write(f"Booking ID: {b['booking_id']}, Name: {b['name']}, Movie: {b['movie_title']}, Showtime: {b['showtime']}, Seats: {', '.join(b['seats'])}")

        elif admin_action == "View Seats Status":
            st.subheader("🪑 View Seats Status")
            if not movies:
                st.info("No movies available.")
            else:
                selected_movie = st.selectbox("Select Movie", [f"{m['title']} (ID: {m['id']})" for m in movies])
                movie_id = int(selected_movie.split("ID: ")[1].rstrip(")"))
                showtimes = get_showtime_for_movie(movie_id)
                if not showtimes:
                    st.info("No showtimes for this movie.")
                else:
                    selected_showtime = st.selectbox("Select Showtime", showtimes)
                    booked_seats = get_booked_seats(movie_id, selected_showtime)
                    available_seats = get_available_seats(movie_id, selected_showtime)
                    st.write("Booked Seats:", ", ".join(booked_seats) if booked_seats else "No seats booked.")
                    st.write("Available Seats:", ", ".join(available_seats) if available_seats else "No seats available.")

        elif admin_action == "View Showtimes":
            st.subheader("⏰ All Showtimes")
            if not movies:
                st.info("No movies available.")
            else:
                for movie in movies:
                    showtimes = get_showtime_for_movie(movie["id"])
                    st.markdown(f"**{movie['title']}**: {', '.join(showtimes) if showtimes else 'No showtimes'}")

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
            st.subheader("📜 Booking History by Name")
            name = st.text_input("Enter Name")
            if name:
                bookings = get_user_bookings(name)
                if not bookings:
                    st.info("No bookings found for this name.")
                else:
                    for b in bookings:
                        st.write(f"Booking ID: {b['booking_id']}, Movie: {b['movie_title']}, Showtime: {b['showtime']}, Seats: {', '.join(b.get('seats', []))}")
