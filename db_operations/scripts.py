from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def get_script_details(userid):
    """Get all tools from user and their count."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    scripts_user = []
    scripts_count = 0
    
    try:
        # Query to fetch all tools
        cursor.execute("SELECT * FROM Scripts WHERE user_id=%s ORDER BY id DESC", (userid, ))
        scripts_user = cursor.fetchall()
        
        # Query to count the tools
        cursor.execute("SELECT COUNT(*) AS count FROM Scripts WHERE user_id=%s ", (userid,))
        scripts_count = cursor.fetchone()['count']
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return scripts_user, scripts_count