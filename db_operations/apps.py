from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

def get_all_apps():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE type_id='3' AND approvedScientific = 1 AND approvedLinguistic = 1 ORDER BY id DESC")
    apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return apps



