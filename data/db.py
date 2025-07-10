# db.py
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        dbname="movie_ticket_db",
        user="postgres",
        password="#5559827898#SS",  # 🔁 use your real password
        host="localhost",
        port="5432"
    )

def run_query(query, params=None, fetch=False):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
    finally:
        conn.close()
