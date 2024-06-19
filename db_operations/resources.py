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

def get_combined_details(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)

    try:
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
                MAX(CASE WHEN tax.title = 'Requisitos Técnicos' THEN t.title END) AS requisitos_tecnicos_title,
                MAX(CASE WHEN tax.title = 'Anos de escolaridade' THEN t.title END) AS anos_escolaridade_title
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

        # Query to fetch script IDs based on resource_id
        script_id_query = """
            SELECT id FROM Scripts WHERE resource_id = %s
        """
        cursor.execute(script_id_query, (resource_id,))
        script_ids = [row['id'] for row in cursor.fetchall()]

        # If there are no scripts, close the connection and return the combined details
        if not script_ids:
            return {
                'resource_details': resource_details,
                'taxonomy_details': taxonomy_details,
                'scripts': {},
                'user_details': {}
            }

        # Query to fetch terms and scripts details
        script_query = """
            SELECT
                Terms.title AS TermTitle,
                Taxonomies.slug AS TaxSlug,
                Scripts.id AS ScriptId,
                Scripts.resource_id AS ResourceId
            FROM
                Terms
            INNER JOIN
                Taxonomies ON Terms.taxonomy_id = Taxonomies.id AND 
                              Taxonomies.slug IN ('macro_areas_resources', 'dominios_resources', 'areas_resources', 'anos_resources', 'subdominios')
            INNER JOIN
                script_terms ON script_terms.term_id = Terms.id
            INNER JOIN
                Scripts ON script_terms.script_id = Scripts.id
            WHERE
                script_terms.script_id IN (%s)
            ORDER BY
                Taxonomies.id ASC, Terms.slug+0 ASC
        """ % ','.join(['%s'] * len(script_ids))

        cursor.execute(script_query, script_ids)
        script_details = cursor.fetchall()

        # Construct scripts dictionary with taxonomy slugs as keys and lists of terms as values
        scripts = {
            'anos_resources': [],
            'areas_resources': [],
            'dominios_resources': [],
            'subdominios': [],
        }

        for script in script_details:
            tax_slug = script.get('TaxSlug')  # Use .get() to safely retrieve TaxSlug
            term_title = script['TermTitle']
            if tax_slug in scripts:
                scripts[tax_slug].append(term_title)

        # Fetch user details associated with script_ids
        user_details = {}
        if script_ids:
            user_query = """
                SELECT u.id AS UserId, u.name AS UserName, u.organization AS UserOrganization
                FROM Users u
                JOIN Scripts s ON u.id = s.user_id
                WHERE s.id IN (%s)
            """ % ','.join(['%s'] * len(script_ids))
            cursor.execute(user_query, script_ids)
            user_details = {row['UserId']: {'name': row['UserName'], 'organization': row['UserOrganization']} for row in cursor.fetchall()}

        # Combine all details into a single dictionary
        combined_details = {}
        if resource_details:
            combined_details.update({
                'resource_id': resource_id,
                'title': resource_details['title'],
                'created_at': resource_details['created_at'],
                'organization': resource_details['organization'],
                'description': resource_details['description'],
                'author': resource_details['author']
            })
        
        if taxonomy_details:
            combined_details.update({
                'idiomas_title': taxonomy_details.get('idiomas_title'),
                'formato_title': taxonomy_details.get('formato_title'),
                'modo_utilizacao_title': taxonomy_details.get('modo_utilizacao_title'),
                'requisitos_tecnicos_title': taxonomy_details.get('requisitos_tecnicos_title'),
                'anos_escolaridade_title': taxonomy_details.get('anos_escolaridade_title')
            })
        
        combined_details['scripts'] = scripts
        combined_details['user_details'] = user_details
        
        return combined_details if combined_details else None

    except mysql.connector.Error as e:
        # Handle database errors
        print(f"Error retrieving combined details: {e}")
        return None
    
    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()







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
