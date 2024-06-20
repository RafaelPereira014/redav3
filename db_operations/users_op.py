from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def get_details(userid):
    """Get the user ID for the given username."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE id=%s", (userid,))
    user = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    return user
    
    