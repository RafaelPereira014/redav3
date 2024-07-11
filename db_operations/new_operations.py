from datetime import datetime
import os
from config import DB_CONFIG  # Import the database configuration
from flask import current_app, session, url_for
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def insert_script(resource_id, user_id, selected_anos, selected_disciplinas, selected_dominios, selected_subdominios, selected_conceitos, outros_conceitos, descricao):
    conn = connect_to_database()
    cursor = conn.cursor()
    current_date = datetime.now()
    
    try:
        # Insert new script
        script_query = """
            INSERT INTO Scripts (resource_id, description, created_at, updated_at, user_id, operation, approved)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(script_query, (resource_id, descricao, current_date, current_date, user_id, descricao, False))
        script_id = cursor.lastrowid
        print(f"Inserted script with ID: {script_id}")

        # Insert associated terms
        term_insert_query = """
            INSERT INTO script_terms (script_id, term_id)
            VALUES (%s, %s)
        """
        
        taxonomies_query = """
            INSERT INTO Terms WHERE slug (anos_resources,areas_resources,dominios_resources,subdominios,hashtags)
            VALUES(%s,%s,%s,%s,%s)
        """
        
        cursor.execute(taxonomies_query,selected_anos,selected_disciplinas,selected_dominios,selected_subdominios,selected_conceitos)

        # Commit the transaction
        conn.commit()

        return script_id

    except mysql.connector.Error as e:
        # Handle database errors
        print(f"Error inserting script: {e}")
        conn.rollback()
        return None

    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
