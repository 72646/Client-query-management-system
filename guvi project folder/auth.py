import hashlib
from db import get_connection

def register_user(username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, hashed_password, role) VALUES (%s,%s,%s)",
        (username, hashed_password, role)
    )
    conn.commit()
    conn.close()

def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND hashed_password=%s",
        (username, hashed_password)
    )
    user = cursor.fetchone()
    conn.close()
    return user
