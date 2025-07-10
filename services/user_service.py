from models.user import User
from data import run_query

class UserService:
    @staticmethod
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = %s;"
        result = run_query(query, (email,), fetch=True)
        if result:
            row = result[0]
            return User(row["id"], row["name"], row["email"], row["is_admin"])
        return None

    @staticmethod
    def create_user(name, email, hashed_password, is_admin=False):
        query = "INSERT INTO users (name, email, password, is_admin) VALUES (%s, %s, %s, %s);"
        run_query(query, (name, email, hashed_password, is_admin))

    @staticmethod
    def get_user_by_id(user_id):
        query = "SELECT * FROM users WHERE id = %s;"
        result = run_query(query, (user_id,), fetch=True)
        if result:
            row = result[0]
            return User(row["id"], row["name"], row["email"], row["is_admin"])
        return None
