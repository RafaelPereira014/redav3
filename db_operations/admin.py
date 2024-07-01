from aifc import Error
from datetime import datetime
import os
from config import DB_CONFIG  # Import the database configuration
from flask import current_app, session, url_for
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

def taxonomies():
    conn = connect_to_database()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT 
        Taxonomy.id, 
        Taxonomy.title, 
        Taxonomy.slug, 
        Taxonomy.locked, 
        Taxonomy.hierarchical, 
        Taxonomy.created_at, 
        Taxonomy.updated_at, 
        Taxonomy.deleted_at, 
        Taxonomy.type_id, 
        Type.id AS Type_id, 
        Type.title AS Type_title, 
        Type.slug AS Type_slug, 
        Type.created_at AS Type_created_at, 
        Type.updated_at AS Type_updated_at, 
        Type.deleted_at AS Type_deleted_at 
    FROM 
        Taxonomies AS Taxonomy 
    LEFT OUTER JOIN 
        Types AS Type 
    ON 
        Taxonomy.type_id = Type.id 
        AND (Type.deleted_at > NOW() OR Type.deleted_at IS NULL) 
    WHERE 
        (Taxonomy.deleted_at > NOW() OR Taxonomy.deleted_at IS NULL) 
        AND Taxonomy.slug NOT IN ('tags_resources', 'tags_apps', 'tags_tools', 'tags_students') 
    ORDER BY 
        Taxonomy.title ASC;
    """
    
    try:
        cursor.execute(query)
        taxonomies = cursor.fetchall()
        return taxonomies
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        if conn.is_connected():
            conn.close()
            
def edit_taxonomie(taxonomy_slug):
    conn = connect_to_database()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
        Term.id, 
        Term.title, 
        Term.slug, 
        Term.icon, 
        Term.color, 
        Term.type, 
        Term.created_at, 
        Term.updated_at, 
        Term.deleted_at, 
        Term.taxonomy_id, 
        Term.parent_id
    FROM 
        Terms AS Term 
    INNER JOIN 
        Taxonomies AS Taxonomy 
    ON 
        Term.taxonomy_id = Taxonomy.id 
        AND ((Taxonomy.deleted_at > NOW() OR Taxonomy.deleted_at IS NULL) AND Taxonomy.slug = %s) 
    WHERE 
        (Term.deleted_at > NOW() OR Term.deleted_at IS NULL) 
    ORDER BY 
        CAST(Term.title AS UNSIGNED) ASC, 
        Term.title ASC, 
        Term.parent_id ASC ;
    """
    
    try:
        cursor.execute(query, (taxonomy_slug,))
        taxonomies = cursor.fetchall()
        return taxonomies
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        if conn.is_connected():
            conn.close()

def get_taxonomy_title(slug):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title FROM Taxonomies WHERE slug=%s", (slug,))
    taxonomy_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if taxonomy_data:
        return taxonomy_data['title']
    else:
        return None  # Handle case where taxonomy with given slug is not found
