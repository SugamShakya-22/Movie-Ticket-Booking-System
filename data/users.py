from db import run_query

def create_user(name, email, hashed_password, is_admin=False):
    query = """
        INSERT INTO users (name, email, password, is_admin)
        VALUES (%s, %s, %s, %s);
    """
    run_query(query, (name, email, hashed_password, is_admin))

def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = %s;"
    result = run_query(query, (email,), fetch=True)
    return result[0] if result else None
