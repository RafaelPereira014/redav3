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
    """Get all tools from user and their count."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    tools_user = []
    tools_count = 0
    
    try:
        # Query to fetch all tools
        cursor.execute("SELECT * FROM Resources WHERE user_id=%s AND type_id=%s ORDER BY id DESC", (userid, 1))
        tools_user = cursor.fetchall()
        
        # Query to count the tools
        cursor.execute("SELECT COUNT(*) AS count FROM Resources WHERE user_id=%s AND type_id=%s", (userid, 1))
        tools_count = cursor.fetchone()['count']
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return tools_user, tools_count



def get_pendent_tools():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE type_id='1' AND approved='0' ORDER BY id DESC")
    pendent_tools = cursor.fetchall()
    cursor.close()
    conn.close()
    return pendent_tools


