from aifc import Error
from datetime import datetime
import os
from config import DB_CONFIG  # Import the database configuration
from flask import current_app, logging, session, url_for
import mysql.connector  # Import MySQL Connector Python module
import logging

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)



def get_userid(username):
    """Get the user ID for the given username."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM Users WHERE name=%s", (username,))
    user = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    
    if user:
        return user['id']
    else:
        return None

def get_user_email(user_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM Users WHERE id=%s", (user_id,))
    user_email = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    
    if user_email:
        return user_email['email']
    else:
        return None

def get_usertype(role_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT type FROM Roles WHERE id=%s", (role_id,))
    user_type = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    
    if user_type:
        return user_type['type']
    else:
        return None

def get_user_password(email):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM Users WHERE email=%s", (email,))
    user_password = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    
    if user_password:
        return user_password['password']
    else:
        return None
    
def create_user(email, password, name, role_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO Users (email, password, name, role_id) 
            VALUES (%s, %s, %s, %s)
        """, (email, password, name, role_id))
        conn.commit()
        logging.info(f"User {name} created successfully.")
    except Exception as e:
        logging.error(f"Error creating user: {e}")
    finally:
        cursor.close()
        conn.close()
        
def delete_user(email):
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM Users where email=%s",(email,))
        conn.commit()
        logging.info(f"User {email} deleted successfully.")
    except Exception as e:
        logging.error(f"Error deleting user: {e}")
    finally:
        cursor.close()
        conn.close()
    
def get_current_month_users():
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        
        data = datetime.now()
        # Get the current year and month
        current_year = data.year
        current_month = data.month
        
        # SQL query to count users created in the current month
        query = """
            SELECT COUNT(*) AS count FROM Users
            WHERE YEAR(created_at) = %s AND MONTH(created_at) = %s
        """
        cursor.execute(query, (current_year, current_month))
        result = cursor.fetchone()
        
        # Extract the count value from the result dictionary
        users_count = result['count'] if result else 0
        
        logging.info(f"Retrieved {users_count} users created in the current month.")
        
        return users_count
    except Exception as e:
        logging.error(f"Error retrieving users for the current month: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
def get_all_users():
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT name,email,organization,created_at,role_id FROM Users ORDER BY id DESC
        """
        cursor.execute(query)
        users = cursor.fetchall()
        
        logging.info(f"Retrieved {len(users)} users from DB.")
        
        return users
    except Exception as e:
        logging.error(f"Error retrieving users for the DB: {e}")
        return None
    finally:
        cursor.close()
        conn.close()