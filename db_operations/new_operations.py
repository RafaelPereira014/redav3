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


def update_script(resource_id, user_id, selected_anos, selected_disciplinas, selected_dominios, selected_subdominios, selected_conceitos, descricao):
    conn = connect_to_database()
    cursor = conn.cursor()
    current_date = datetime.now()

    try:
        # Update existing script
        script_query = """
            UPDATE Scripts 
            SET description = %s, updated_at = %s, user_id = %s, operation = %s, approved = %s
            WHERE resource_id = %s
        """
        cursor.execute(script_query, (descricao, current_date, user_id, descricao, False, resource_id))
        print(f"Updated script with resource ID: {resource_id}")

        # Get the script ID from the resource ID
        cursor.execute("SELECT id FROM Scripts WHERE resource_id = %s", (resource_id,))
        script_row = cursor.fetchone()
        if not script_row:
            print(f"No script found for resource ID: {resource_id}")
            return None
        script_id = script_row[0]

        def update_terms(term_list, taxonomy_slug):
            # Remove existing terms
            delete_terms_query = """
                DELETE FROM script_terms 
                WHERE script_id = %s AND term_id IN (
                    SELECT id FROM Terms WHERE taxonomy_id = (SELECT id FROM Taxonomies WHERE slug = %s)
                )
            """
            cursor.execute(delete_terms_query, (script_id, taxonomy_slug))

            # Insert updated terms
            term_insert_query = """
                INSERT INTO script_terms (script_id, term_id, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
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

        # Update associated terms
        update_terms(selected_anos, 'anos_resources')
        update_terms(selected_disciplinas, 'areas_resources')
        update_terms(selected_dominios, 'dominios_resources')
        update_terms(selected_subdominios, 'subdominios')
        update_terms(selected_conceitos, 'hashtags')

        # Commit the transaction
        conn.commit()

        return script_id

    except mysql.connector.Error as e:
        # Handle database errors
        print(f"Error updating script: {e}")
        conn.rollback()
        return None

    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_resource_and_scripts(resource_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Call the stored procedure
        cursor.callproc('DeleteResourceAndScripts', (resource_id,))
        
        # Commit the transaction
        conn.commit()

        print(f"Resource and associated scripts with ID {resource_id} have been deleted.")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        conn.rollback()  # Rollback the transaction on error

    finally:
        cursor.close()
        conn.close()