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
            email VARCHAR(255) NOT NULL,
            password VARCHAR(150) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            username VARCHAR(150),
            score INTEGER,
            total_questions INTEGER,
            taken_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def insert_user(username, email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, password)
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

def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def save_quiz_result(username, score, total_questions):
    """
    Save a quiz result for a user.
    
    Args:
        username: Username of the person who took the quiz
        score: Number of questions they got correct
        total_questions: Total number of questions in the quiz
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Get user_id from username
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    
    if not user:
        cur.close()
        conn.close()
        return False  # User not found
    
    user_id = user[0]
    
    # Insert quiz result
    cur.execute(
        """
        INSERT INTO quiz_results (user_id, username, score, total_questions)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, username, score, total_questions)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    return True

def get_quiz_history(username):
    """
    Get all quiz results for a user, plus their average.
    
    Args:
        username: Username to get history for
        
    Returns:
        Dictionary with:
        - 'quizzes': List of quiz results (date, score, total)
        - 'average': Average score as percentage
        - 'total_quizzes': How many quizzes taken
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Get all quiz results for this user
    cur.execute(
        """
        SELECT score, total_questions, taken_at
        FROM quiz_results
        WHERE username = %s
        ORDER BY taken_at DESC
        """,
        (username,)
    )
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    if not results:
        # No quizzes taken yet
        return {
            'quizzes': [],
            'average': 0,
            'total_quizzes': 0
        }
    
    # Calculate average percentage
    total_score = 0
    total_possible = 0
    
    quizzes = []
    for score, total_questions, taken_at in results:
        total_score += score
        total_possible += total_questions
        
        # Calculate percentage for this quiz
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        quizzes.append({
            'score': score,
            'total': total_questions,
            'percentage': round(percentage, 1),
            'date': taken_at
        })
    
    # Calculate overall average
    average = (total_score / total_possible * 100) if total_possible > 0 else 0
    
    return {
        'quizzes': quizzes,
        'average': round(average, 1),
        'total_quizzes': len(results)
    }