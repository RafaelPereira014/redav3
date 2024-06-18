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

def get_apps_from_user(userid):
    """Get all apps from user."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM Resources WHERE user_id=%s AND type_id=%s ORDER BY id DESC", (userid, 3))
        apps_user = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        apps_user = []
    finally:
        cursor.close()
        conn.close()
    
    return apps_user



