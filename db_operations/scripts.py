from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)





def get_script_details():
    """Get all tools from user and their count."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    scripts_user = []
    scripts_count = 0
    
    try:
        # Query to fetch all tools
        cursor.execute("SELECT * FROM Scripts  ORDER BY id DESC")
        scripts_user = cursor.fetchall()
        
        # Query to count the tools
        cursor.execute("SELECT COUNT(*) AS count FROM Scripts ")
        scripts_count = cursor.fetchone()['count']
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return scripts_user, scripts_count



def get_script_details_by_user(user_id):
    """Get all tools from user and their count."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    scripts_user = []
    scripts_count = 0
    
    try:
        # Query to fetch all tools
        cursor.execute("SELECT * FROM Scripts WHERE user_id=%s  ORDER BY id DESC",(user_id,))
        scripts_user = cursor.fetchall()
        
        # Query to count the tools
        cursor.execute("SELECT COUNT(*) AS count FROM Scripts ")
        scripts_count = cursor.fetchone()['count']
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return scripts_user, scripts_count


def get_script_details_pendent():
    """Get all tools from user and their count."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    scripts_user = []
    scripts_count = 0
    
    try:
        # Query to fetch all tools
        cursor.execute("SELECT * FROM Scripts WHERE approved='0' ORDER BY id DESC")
        scripts_user = cursor.fetchall()
        
        # Query to count the tools
        cursor.execute("SELECT COUNT(*) AS count FROM Scripts ")
        scripts_count = cursor.fetchone()['count']
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return scripts_user, scripts_count


def get_script_id_by_description(description):
    conn = connect_to_database()  # Connect to the database
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Execute the SQL query to find the script ID by description
        query = "SELECT id FROM Scripts WHERE description = %s"
        cursor.execute(query, (description,))
        result = cursor.fetchone()
        
        # If a result is found, return the script ID
        if result:
            return result['script_id']
        else:
            return None  # Return None if no matching script is found
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


