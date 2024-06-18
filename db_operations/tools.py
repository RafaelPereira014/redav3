from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

def get_all_tools():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE type_id='1' AND approvedScientific = 1 AND approvedLinguistic = 1 ORDER BY id DESC")
    tools = cursor.fetchall()
    cursor.close()
    conn.close()
    return tools

def get_tools_from_user(userid):
    """Get all tools from user."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM Resources WHERE user_id=%s AND type_id=%s ORDER BY id DESC", (userid, 1))
        tools_user = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        tools_user = []
    finally:
        cursor.close()
        conn.close()
    
    return tools_user



