# auth.py
from data.users import create_user, get_user_by_email
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def register_user(name, email, password, is_admin=False):
    hashed = hash_password(password)
    create_user(name, email, hashed, is_admin)

def get_user(email):
    return get_user_by_email(email)
