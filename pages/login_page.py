# pages/login_page.py

import streamlit as st
from auth import get_user_by_email, verify_password, create_user


class LoginPage:
    def __init__(self):
        self.user = None

    def render(self):
        auth_action = st.sidebar.radio("Login or Register", ["Login", "Register"])

        if auth_action == "Register":
            st.sidebar.subheader("Create Account")
            name = st.sidebar.text_input("Name")
            email = st.sidebar.text_input("Email")
            password = st.sidebar.text_input("Password", type="password")
            retype = st.sidebar.text_input("Retype Password", type="password")

            if st.sidebar.button("Register"):
                if name and email and password == retype:
                    existing_user = get_user_by_email(email)
                    if existing_user:
                        st.sidebar.error("User already exists.")
                    else:
                        is_admin = email.lower() == "admin@hotmail.com"
                        create_user(name, email, password, is_admin)
                        st.sidebar.success("Registered successfully. Please log in.")
                else:
                    st.sidebar.warning("Please fill all fields.")

        else:
            st.sidebar.subheader("Login")
            email = st.sidebar.text_input("Email")
            password = st.sidebar.text_input("Password", type="password")

            if st.sidebar.button("Login"):
                user = get_user_by_email(email)
                if not user:
                    st.sidebar.error("User not found.")
                elif not verify_password(password, user["password"]):
                    st.sidebar.error("Invalid credentials.")
                else:
                    self.user = user
                    st.session_state.user = user
                    st.experimental_rerun()
