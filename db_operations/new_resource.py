from datetime import datetime
import os
from config import DB_CONFIG  # Import the database configuration
from flask import current_app, session, url_for
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

def get_formatos():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT
            t.title AS formato_title
        FROM
            resource_terms rt
        JOIN
            Terms t ON rt.term_id = t.id
        JOIN
            Taxonomies tax ON t.taxonomy_id = tax.id
        WHERE
            tax.title = 'Formato'
    """)
    formatos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tuple(item['formato_title'] for item in formatos)

def get_idiomas():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT
            t.title AS idiomas_title
        FROM
            resource_terms rt
        JOIN
            Terms t ON rt.term_id = t.id
        JOIN
            Taxonomies tax ON t.taxonomy_id = tax.id
        WHERE
            tax.title = 'Idiomas'
    """)
    idiomas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tuple(item['idiomas_title'] for item in idiomas)

def get_modos_utilizacao():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT
            t.title AS modo_utilizacao_title
        FROM
            resource_terms rt
        JOIN
            Terms t ON rt.term_id = t.id
        JOIN
            Taxonomies tax ON t.taxonomy_id = tax.id
        WHERE
            tax.title = 'Modos de utilização'
    """)
    modos_utilizacao = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tuple(item['modo_utilizacao_title'] for item in modos_utilizacao)

def get_requisitos_tecnicos():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT
            t.title AS requisitos_tecnicos_title
        FROM
            resource_terms rt
        JOIN
            Terms t ON rt.term_id = t.id
        JOIN
            Taxonomies tax ON t.taxonomy_id = tax.id
        WHERE
            tax.title = 'Requisitos técnicos'
    """)
    requisitos_tecnicos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tuple(item['requisitos_tecnicos_title'] for item in requisitos_tecnicos)

def get_anos_escolaridade():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT
            t.title AS anos_escolaridade_title
        FROM
            resource_terms rt
        JOIN
            Terms t ON rt.term_id = t.id
        JOIN
            Taxonomies tax ON t.taxonomy_id = tax.id
        WHERE
            tax.title = 'Anos escolaridade'
    """)
    anos_escolaridade = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tuple(item['anos_escolaridade_title'] for item in anos_escolaridade)


def get_unique_terms(level):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    query = f"""
    SELECT DISTINCT
        tx.title AS term_title
    FROM redav3.TermRelationships tr
    INNER JOIN terms_relations trs ON trs.term_relationship_id = tr.id
    INNER JOIN Terms tx ON tx.id = trs.term_id
    WHERE trs.level = {level}
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    conn.close()
    return [row['term_title'] for row in result]

def get_filtered_terms(level, parent_level, parent_term):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    query = f"""
    SELECT DISTINCT
        tx.title AS term_title
    FROM redav3.TermRelationships tr
    INNER JOIN terms_relations trs ON trs.term_relationship_id = tr.id
    INNER JOIN Terms tx ON tx.id = trs.term_id
    WHERE trs.level = {level} AND
          trs.term_relationship_id IN (
              SELECT tr.id
              FROM redav3.TermRelationships tr
              INNER JOIN terms_relations trs ON trs.term_relationship_id = tr.id
              INNER JOIN Terms tx ON tx.id = trs.term_id
              WHERE trs.level = {parent_level} AND tx.title = %s
          )
    ORDER BY tx.title
    """
    
    cursor.execute(query, (parent_term,))
    result = cursor.fetchall()
    
    conn.close()
    return [row['term_title'] for row in result]


def create_resource(title,autor,org,descricao):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    insert_query = """
        INSERT INTO resources (title, autor, organizacao, descricao)
        VALUES (%s, %s, %s, %s)
        """
    # Execute the insert query
    cursor.execute(insert_query, (title, autor, org, descricao))
    
    # Commit the transaction
    conn.commit()
    
    cursor.close()
    conn.close()


def create_new_resource(title, author, organization, description, idiomas_title=None, formato_title=None, modo_utilizacao_title=None, requisitos_tecnicos_title=None, anos_escolaridade_title=None, scripts_by_id=None):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        # Insert into Resources table
        insert_query = """
            INSERT INTO Resources (title, author, organization, description)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (title, author, organization, description))
        resource_id = cursor.lastrowid  # Get the last inserted resource ID

        # Insert into Taxonomy details if provided
        if idiomas_title:
            insert_taxonomy_query = """
                INSERT INTO resource_terms (resource_id, term_id)
                SELECT %s, t.id FROM Terms t
                JOIN Taxonomies tax ON t.taxonomy_id = tax.id
                WHERE t.title = %s AND tax.title = 'Idiomas'
            """
            cursor.execute(insert_taxonomy_query, (resource_id, idiomas_title))

        if formato_title:
            insert_taxonomy_query = """
                INSERT INTO resource_terms (resource_id, term_id)
                SELECT %s, t.id FROM Terms t
                JOIN Taxonomies tax ON t.taxonomy_id = tax.id
                WHERE t.title = %s AND tax.title = 'Formato'
            """
            cursor.execute(insert_taxonomy_query, (resource_id, formato_title))

        if modo_utilizacao_title:
            insert_taxonomy_query = """
                INSERT INTO resource_terms (resource_id, term_id)
                SELECT %s, t.id FROM Terms t
                JOIN Taxonomies tax ON t.taxonomy_id = tax.id
                WHERE t.title = %s AND tax.title = 'Modos de utilização'
            """
            cursor.execute(insert_taxonomy_query, (resource_id, modo_utilizacao_title))

        if requisitos_tecnicos_title:
            insert_taxonomy_query = """
                INSERT INTO resource_terms (resource_id, term_id)
                SELECT %s, t.id FROM Terms t
                JOIN Taxonomies tax ON t.taxonomy_id = tax.id
                WHERE t.title = %s AND tax.title = 'Requisitos Técnicos'
            """
            cursor.execute(insert_taxonomy_query, (resource_id, requisitos_tecnicos_title))

        if anos_escolaridade_title:
            insert_taxonomy_query = """
                INSERT INTO resource_terms (resource_id, term_id)
                SELECT %s, t.id FROM Terms t
                JOIN Taxonomies tax ON t.taxonomy_id = tax.id
                WHERE t.title = %s AND tax.title = 'Anos de escolaridade'
            """
            cursor.execute(insert_taxonomy_query, (resource_id, anos_escolaridade_title))

        # Insert into Scripts table
        if scripts_by_id:
            for script_id, script_details in scripts_by_id.items():
                operation = script_details.get('operation')
                user_id = script_details.get('user_id')

                if operation and user_id:
                    insert_script_query = """
                        INSERT INTO Scripts (resource_id, operation, user_id)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_script_query, (resource_id, operation, user_id))
                    script_id = cursor.lastrowid

                    # Insert script terms
                    for taxonomy_slug, terms in script_details.items():
                        if taxonomy_slug in ('idiomas', 'formato', 'modo_utilizacao', 'requisitos_tecnicos', 'anos_escolaridade'):
                            for term in terms:
                                insert_script_term_query = """
                                    INSERT INTO script_terms (script_id, term_id)
                                    SELECT %s, t.id FROM Terms t
                                    JOIN Taxonomies tax ON t.taxonomy_id = tax.id
                                    WHERE t.title = %s AND tax.title = %s
                                """
                                cursor.execute(insert_script_term_query, (script_id, term, taxonomy_slug))

        # Commit the transaction
        conn.commit()

        return resource_id  # Return the newly inserted resource ID

    except mysql.connector.Error as e:
        # Handle database errors
        print(f"Error creating new resource: {e}")
        return None

    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
