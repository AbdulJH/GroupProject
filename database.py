import psycopg2
def insert_user(username, password):
    conn = psycopg2.connect(
        dbname="ics499db",
        user="postgres",
        password="",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )
    conn.commit()
    cur.close()
    conn.close()

def check_user(username):
    conn = psycopg2.connect(
        dbname="ics499db",
        user="postgres",
        password="",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE username = %s",
        (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

def valid_login(username, password):
    conn = psycopg2.connect(
        dbname="ics499db",
        user="postgres",
        password="",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE username = %s AND password = %s",
        (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

