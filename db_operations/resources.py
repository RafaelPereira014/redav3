from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def get_recent_approved_resources(limit=8):
    """Get the most recent approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE approvedScientific = 1 AND approvedLinguistic = 1 ORDER BY id DESC LIMIT %s", (limit,))
    resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return resources

def get_all_resources():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE approvedScientific = 1 AND approvedLinguistic = 1 ORDER BY id DESC")
    resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return resources


def approved_resources():
    return 

def has_more_than_25_characters(string):
    """
    Check if a string has more than 25 characters.
    
    Parameters:
        string (str): The input string to check.
        
    Returns:
        bool: True if the string has more than 25 characters, False otherwise.
    """
    return len(string) > 25


def cut_string(text):
    if len(text) > 25:
        return text[:25] + "..."
    else:
        return text
