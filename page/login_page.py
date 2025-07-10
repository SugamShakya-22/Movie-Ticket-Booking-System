import streamlit as st
from auth import get_user, verify_password, register_user, login


class LoginPage:
    def __init__(self):
        self.user = None

    def render(self):
        auth_action = st.sidebar.radio("Login or Register", ["Login", "Register"])

        if auth_action == "Register":
            st.sidebar.subheader("Create Account")
            name = st.sidebar.text_input("Name").strip()
            email = st.sidebar.text_input("Email").strip()
            password = st.sidebar.text_input("Password", type="password")
            retype = st.sidebar.text_input("Retype Password", type="password")

            if st.sidebar.button("Register"):
                if not (name and email and password and retype):
                    st.sidebar.warning("Please fill all fields.")
                elif password != retype:
                    st.sidebar.error("Passwords do not match.")
                else:
                    existing_user = get_user(email)
                    if existing_user:
                        st.sidebar.error("User already exists.")
                    else:
                        is_admin = email.lower() == "admin@hotmail.com"
                        register_user(name, email, password, is_admin)
                        st.sidebar.success("Registered successfully. Please log in.")
                        # Optional: clear input fields here by rerunning or managing state

        else:  # Login
            st.sidebar.subheader("Login")
            email = st.sidebar.text_input("Email").strip()
            password = st.sidebar.text_input("Password", type="password")

            st.sidebar.subheader("Login")
            email = st.sidebar.text_input("Email").strip()
            password = st.sidebar.text_input("Password", type="password")

            if st.sidebar.button("Login"):
                if login(email, password):
                    st.rerun()
                else:
                    st.sidebar.error("Invalid email or password.")
