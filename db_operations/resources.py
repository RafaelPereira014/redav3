from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

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

def get_all_resources():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE approvedScientific = 1 AND approvedLinguistic = 1 ORDER BY id DESC")
    resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return resources

def get_pendent_resources():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE approvedScientific = 1 AND approvedLinguistic = 0 OR approvedScientific = 0 AND approvedLinguistic = 1 ORDER BY id DESC")
    pendent_resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return pendent_resources

def get_hidden_resources():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE hidden='1' ORDER BY id DESC")
    hidden_resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return hidden_resources


def get_highlighted_resources():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE highlight='1' ORDER BY id DESC")
    highlighted_resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return highlighted_resources

def get_recent_approved_resources(limit=8):
    """Get the most recent approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE approvedScientific = 1 AND approvedLinguistic = 1 ORDER BY id DESC LIMIT %s", (limit,))
    resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return resources


def get_resources_from_user(userid):
    """Get all resources from user."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM Resources WHERE user_id=%s ORDER BY id DESC", (userid,))
        resources_user = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        resources_user = []
    finally:
        cursor.close()
        conn.close()
    
    return resources_user

def get_resource_and_taxonomy_details(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    # Query to fetch resource details
    resource_query = """
        SELECT * FROM Resources WHERE id = %s
    """
    cursor.execute(resource_query, (resource_id,))
    resource_details = cursor.fetchone()
    
    # Query to fetch taxonomy details
    taxonomy_query = """
        SELECT
            rt.resource_id,
            MAX(CASE WHEN tax.title = 'Idiomas' THEN t.title END) AS idiomas_title,
            MAX(CASE WHEN tax.title = 'Formato' THEN t.title END) AS formato_title,
            MAX(CASE WHEN tax.title = 'Modos de utilização' THEN t.title END) AS modo_utilizacao_title,
            MAX(CASE WHEN tax.title = 'Requisitos Técnicos' THEN t.title END) AS requisitos_tecnicos_title
        FROM
            resource_terms rt
        JOIN
            Terms t ON rt.term_id = t.id
        JOIN
            Taxonomies tax ON t.taxonomy_id = tax.id
        WHERE
            rt.resource_id = %s
        GROUP BY
            rt.resource_id;
    """
    cursor.execute(taxonomy_query, (resource_id,))
    taxonomy_details = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    # Combine both resource and taxonomy details into a single dictionary
    if resource_details and taxonomy_details:
        combined_details = {
            'resource_id': resource_id,
            'title': resource_details['title'],
            'description': resource_details['description'],
            'idiomas_title': taxonomy_details['idiomas_title'],
            'formato_title': taxonomy_details['formato_title'],
            'modo_utilizacao_title': taxonomy_details['modo_utilizacao_title'],
            'requisitos_tecnicos_title': taxonomy_details['requisitos_tecnicos_title']
            # Add more fields as needed
        }
        return combined_details
    else:
        return None  # Or handle the case where details are not found




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
