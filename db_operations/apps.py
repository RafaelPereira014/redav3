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

def get_apps():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE type_id='3'  ORDER BY id DESC")
    all_apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_apps

def get_apps_from_user(userid):
    """Get all tools from user and their count."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    apps_user = []
    apps_count = 0
    
    try:
        # Query to fetch all tools
        cursor.execute("SELECT * FROM Resources WHERE user_id=%s AND type_id=%s ORDER BY id DESC", (userid, 3))
        apps_user = cursor.fetchall()
        
        # Query to count the tools
        cursor.execute("SELECT COUNT(*) AS count FROM Resources WHERE user_id=%s AND type_id=%s", (userid, 3))
        apps_count = cursor.fetchone()['count']
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return apps_user, apps_count

def get_pendent_apps():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE type_id='3' AND approved='0' ORDER BY id DESC")
    pendent_apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return pendent_apps


