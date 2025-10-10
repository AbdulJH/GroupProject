import psycopg2
import os

DB_NAME = os.environ.get("DB_NAME", "ics499db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "db")

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

def create_users_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(150) UNIQUE NOT NULL,
            password VARCHAR(150) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )
    conn.commit()
    cur.close()
    conn.close()

def check_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE username = %s",
        (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

def valid_login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE username = %s AND password = %s",
        (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

