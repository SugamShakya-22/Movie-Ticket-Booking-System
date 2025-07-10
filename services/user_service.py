# user_service.py

from models.user import User
from data.db import run_query

class UserService:
    @staticmethod
    def get_user_by_email(email: str):
        """Fetch a user by email from the database."""
        query = "SELECT * FROM users WHERE email = %s;"
        result = run_query(query, (email,), fetch=True)
        if result:
            row = result[0]
            return User(row["id"], row["name"], row["email"], row["is_admin"], row["password"])
        return None

    @staticmethod
    def create_user(name: str, email: str, hashed_password: str, is_admin: bool = False):
        """Create a new user with the given details."""
        query = """
            INSERT INTO users (name, email, password, is_admin)
            VALUES (%s, %s, %s, %s);
        """
        run_query(query, (name, email, hashed_password, is_admin))
