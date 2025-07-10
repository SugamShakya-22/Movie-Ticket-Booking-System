# main.py
import streamlit as st

from pages.browse_movies_page import BrowseMoviesPage
from pages.booking_page import BookingPage
from pages.cancel_booking_page import CancelBookingPage
from pages.admin_panel import AdminPanel
from auth import get_user, register_user, verify_password

st.set_page_config(page_title="Movie Ticket Booking", layout="centered")
st.title("🎬 Movie Ticket Booking System")

# Initialize session state for user
if "user" not in st.session_state:
    st.session_state.user = None

def login_flow():
    st.sidebar.subheader("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        user = get_user(email)
        if not user:
            st.sidebar.error("User not found.")
        elif not verify_password(password, user.password):
            st.sidebar.error("Invalid credentials.")
        else:
            st.session_state.user = {
                "id": user.user_id,
                "name": user.name,
                "email": user.email,
                "is_admin": user.is_admin
            }
            st.rerun()

def register_flow():
    st.sidebar.subheader("Register")
    name = st.sidebar.text_input("Name")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    re_password = st.sidebar.text_input("Confirm Password", type="password")

    if st.sidebar.button("Register"):
        if not (name and email and password and re_password):
            st.sidebar.warning("Please fill all fields.")
        elif password != re_password:
            st.sidebar.warning("Passwords do not match.")
        else:
            existing_user = get_user(email)
            if existing_user:
                st.sidebar.error("User already exists.")
            else:
                register_user(name, email, password, is_admin=(email.lower() == "admin@hotmail.com"))
                st.sidebar.success("Registration successful! Please login.")

# Authentication UI
if st.session_state.user is None:
    auth_option = st.sidebar.radio("Choose action", ["Login", "Register"])
    if auth_option == "Login":
        login_flow()
    else:
        register_flow()
else:
    st.sidebar.success(f"Logged in as {st.session_state.user['name']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# Menu & page routing
if st.session_state.user:
    menu = ["Browse Movies", "Book Tickets", "Cancel Booking"]
    if st.session_state.user.get("is_admin"):
        menu.append("Admin Panel")

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Browse Movies":
        BrowseMoviesPage().render()
    elif choice == "Book Tickets":
        BookingPage().render()
    elif choice == "Cancel Booking":
        CancelBookingPage().render()
    elif choice == "Admin Panel":
        AdminPanel().render()
else:
    st.info("Please login or register to continue.")
