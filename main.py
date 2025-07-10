# main.py
import streamlit as st

from pages.browse_movies_page import BrowseMoviesPage
from pages.booking_page import BookingPage
from pages.cancel_booking_page import CancelBookingPage
from pages.admin_panel import AdminPanel
from booking_logic import confirm_booking, get_all_bookings, get_user_bookings, cancel_user_booking
from admin_logic import add_new_movie, remove_movie_by_id, update_movie_showtime, add_movie_showtime, remove_movie_showtime, list_movies, list_showtime
from auth import register_user, get_user, verify_password

# Authentication logic here (assuming st.session_state.user is set)

st.set_page_config(page_title="Movie Ticket Booking", layout="centered")
st.title("🎬 Movie Ticket Booking System")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user:
    st.sidebar.success(f"Logged in as {st.session_state.user['name']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()

menu = []
if st.session_state.user:
    menu = ["Browse Movies", "Book Tickets", "Cancel Booking"]
    if st.session_state.user.get("is_admin"):
        menu.append("Admin")

choice = st.sidebar.selectbox("Menu", menu) if menu else None

if choice == "Browse Movies":
    BrowseMoviesPage().render()
elif choice == "Book Tickets":
    BookingPage().render()
elif choice == "Cancel Booking":
    CancelBookingPage().render()
elif choice == "Admin":
    AdminPanel().render()
else:
    if not st.session_state.user:
        st.info("Please login to continue.")
