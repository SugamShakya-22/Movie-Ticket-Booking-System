from services.user_service import UserService
from passlib.context import CryptContext
import streamlit as st

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def register_user(name, email, password, is_admin=False):
    hashed = hash_password(password)
    UserService.create_user(name, email, hashed, is_admin)

def get_user(email):
    return UserService.get_user_by_email(email)


def login(email, password):
    user = get_user(email)
    if user and verify_password(password, user["password"]):
        st.session_state["user_id"] = user["id"]
        st.session_state["name"] = user["name"]
        st.session_state["role"] = "admin" if user["is_admin"] else "user"
        return True
    return False

