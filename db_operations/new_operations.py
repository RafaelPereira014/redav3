from datetime import datetime
import os
from config import DB_CONFIG  # Import the database configuration
from flask import current_app, session, url_for
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def insert_script(resource_id, user_id, selected_anos, selected_disciplinas, selected_dominios, selected_subdominios, selected_conceitos,  descricao):
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

        def insert_terms(term_list, taxonomy_slug):
            term_insert_query = """
            INSERT INTO script_terms (script_id, term_id,created_at,updated_at)
            VALUES (%s, %s,NOW(),NOW())
            """
            for term in term_list:
                # Fetch term_id from Terms table
                get_term_id_query = """
                    SELECT id FROM Terms WHERE title = %s AND taxonomy_id = (SELECT id FROM Taxonomies WHERE slug = %s)
                """
                cursor.execute(get_term_id_query, (term, taxonomy_slug))
                term_row = cursor.fetchone()
                if term_row:
                    term_id = term_row[0]  # Accessing the first element of the tuple (assuming id is the first column)
                    cursor.execute(term_insert_query, (script_id, term_id))
                else:
                    print(f"Term '{term}' for taxonomy '{taxonomy_slug}' not found in database.")

        # Insert associated terms
        insert_terms(selected_anos, 'anos_resources')
        insert_terms(selected_disciplinas, 'areas_resources')
        insert_terms(selected_dominios, 'dominios_resources')
        insert_terms(selected_subdominios, 'subdominios')
        insert_terms(selected_conceitos, 'hashtags')
        
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


