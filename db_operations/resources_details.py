from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def taxonomie_details(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    query = """
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
    
    cursor.execute(query, (resource_id,))
    resource_details = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return resource_details
