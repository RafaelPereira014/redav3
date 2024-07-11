from datetime import datetime
import logging
import os
import re
from config import DB_CONFIG  # Import the database configuration
from flask import current_app, session, url_for
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
    
def get_username(user_id):
    """Get the user ID for the given username."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM Users WHERE id=%s", (user_id,))
    username = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    
    if username:
        return username['name']
    else:
        return None

def get_all_resources(page, per_page):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    offset = (page - 1) * per_page

    query = """
        SELECT * FROM Resources WHERE (approvedScientific = 1 AND approvedLinguistic = 1)  AND type_id='2' AND hidden='0'
        ORDER BY id DESC
        LIMIT %s OFFSET %s
    """
    
    cursor.execute(query, (per_page, offset))
    resources = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return resources

def get_total_resource_count():
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = "SELECT COUNT(*) FROM Resources where type_id='2'"
    
    cursor.execute(query)
    total_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return total_count


def get_pendent_resources():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE (approvedScientific = 1 AND approvedLinguistic = 0) OR (approvedScientific = 0 AND approvedLinguistic = 1) OR (approvedScientific = 0 AND approvedLinguistic = 0) ORDER BY id DESC")
    pendent_resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return pendent_resources

def update_approvedScientific(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE Resources set approvedScientific='1' where id=%s",(resource_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
def update_approvedLinguistic(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE Resources set approvedLinguistic='1' where id=%s",(resource_id,))
    conn.commit()
    cursor.close()
    conn.close()

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
    cursor.execute("SELECT id,title,description FROM Resources WHERE highlight='1' ORDER BY id DESC")
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

        # Query to fetch script IDs, associated taxonomies, and operation
        script_query = """
            SELECT
                Scripts.id AS ScriptId,
                Scripts.resource_id AS ResourceId,
                Scripts.operation AS Operation,
                Scripts.approved AS Approved,
                Scripts.user_id AS UserId,
                Terms.title AS TermTitle,
                Taxonomies.slug AS TaxSlug
            FROM
                Scripts
            LEFT JOIN
                script_terms ON Scripts.id = script_terms.script_id
            LEFT JOIN
                Terms ON script_terms.term_id = Terms.id
            LEFT JOIN
                Taxonomies ON Terms.taxonomy_id = Taxonomies.id
            WHERE
                Scripts.resource_id = %s
            AND
                Taxonomies.slug IN ('macro_areas_resources', 'dominios_resources', 'areas_resources', 'anos_resources', 'subdominios', 'hashtags')
            ORDER BY
                Taxonomies.id ASC, Terms.slug+0 ASC;
        """
        cursor.execute(script_query, (resource_id,))
        script_details = cursor.fetchall()

        # Prepare a dictionary to store scripts grouped by script id and taxonomy slugs
        scripts_by_id = {}
        user_ids = []
        for script in script_details:
            script_id = script['ScriptId']
            user_id = script['UserId']
            tax_slug = script['TaxSlug']
            term_title = script['TermTitle']
            operation = script['Operation']
            approved = script['Approved']

            if script_id not in scripts_by_id:
                scripts_by_id[script_id] = {
                    'operation': operation,
                    'user_id': user_id,
                    'approved': approved,
                    'idiomas': [],
                    'anos_resources': [],
                    'formato': [],
                    'modo_utilizacao': [],
                    'requisitos_tecnicos': [],
                    'anos_escolaridade': [],
                    'areas_resources': [],
                    'dominios_resources': [],
                    'macro_areas': [],
                    'subdominios': [],
                    'hashtags': []
                }
                user_ids.append(user_id)
            scripts_by_id[script_id][tax_slug].append(term_title)

        # Fetch user details associated with the scripts
        user_details = {}
        if user_ids:
            user_query = """
                SELECT u.id AS UserId, u.name AS UserName, u.organization AS UserOrganization
                FROM Users u
                WHERE u.id IN ({})
            """.format(','.join(map(str, user_ids)))
            cursor.execute(user_query)
            user_details = {row['UserId']: {'name': row['UserName'], 'organization': row['UserOrganization']} for row in cursor.fetchall()}

        # Combine all details into a single dictionary
        combined_details = {}
        if resource_details:
            combined_details.update({
                'resource_id': resource_id,
                'title': resource_details['title'],
                'approvedScientific': resource_details['approvedScientific'],
                'approvedLinguistic': resource_details['approvedLinguistic'],
                'hidden': resource_details['hidden'],
                'created_at': resource_details['created_at'],
                'organization': resource_details['organization'],
                'description': resource_details['description'],
                'author': resource_details['author'],
                'user_id': resource_details['user_id']
            })

        if taxonomy_details:
            combined_details.update({
                'idiomas_title': taxonomy_details.get('idiomas_title'),
                'formato_title': taxonomy_details.get('formato_title'),
                'modo_utilizacao_title': taxonomy_details.get('modo_utilizacao_title'),
                'requisitos_tecnicos_title': taxonomy_details.get('requisitos_tecnicos_title'),
                'anos_escolaridade_title': taxonomy_details.get('anos_escolaridade_title')
            })

        combined_details['scripts_by_id'] = scripts_by_id
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


def insert_resource_details(cursor, resource_details):
    resource_insert_query = """
        INSERT INTO Resources 
        (title, slug, description, operation, operation_author, techResources, email, organization, 
        duration, highlight, exclusive, embed, link, author, approved, approvedScientific, approvedLinguistic, 
        status, accepted_terms, created_at, updated_at, deleted_at, user_id, type_id, image_id, hidden)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    resource_data = (
        resource_details['title'],
        resource_details['slug'],  # Make sure resource_details includes 'slug' key
        resource_details['description'],
        resource_details['operation'],
        resource_details['operation_author'],
        resource_details['techResources'],
        resource_details['email'],
        resource_details['organization'],
        resource_details['duration'],
        resource_details['highlight'],
        resource_details['exclusive'],
        resource_details['embed'],
        resource_details['link'],
        resource_details['author'],
        resource_details['approved'],
        resource_details['approvedScientific'],
        resource_details['approvedLinguistic'],
        resource_details['status'],
        resource_details['accepted_terms'],
        resource_details['created_at'],
        resource_details['updated_at'],
        resource_details['deleted_at'],
        resource_details['user_id'],
        resource_details['type_id'],
        resource_details['image_id'],
        resource_details['hidden']
    )
    cursor.execute(resource_insert_query, resource_data)
    return cursor.lastrowid

def insert_taxonomy_details(cursor,resource_id, taxonomy_details):
    taxonomy_insert_query = """
        INSERT INTO Terms (title, taxonomy_id, created_at, updated_at)
        VALUES (%s, %s, NOW(), NOW())
    """
    
    taxonomy_data = [
        (taxonomy_details['idiomas_title'], get_taxonomy_id_for_title('Idiomas')),
        (taxonomy_details['formato_title'], get_taxonomy_id_for_title('Formato')),
        (taxonomy_details['modo_utilizacao_title'], get_taxonomy_id_for_title('Modos de utilização')),
        (taxonomy_details['requisitos_tecnicos_title'], get_taxonomy_id_for_title('Requisitos Técnicos')),
        (taxonomy_details['anos_escolaridade_title'], get_taxonomy_id_for_title('Anos de escolaridade'))
    ]

    for data in taxonomy_data:
        cursor.execute(taxonomy_insert_query, data)
        term_id = cursor.lastrowid

        # Insert into resource_terms
        resource_term_insert_query = """
            INSERT INTO resource_terms (resource_id, term_id,created_at,updated_at)
            VALUES (%s, %s,NOW(),NOW())
        """
        resource_term_data = (resource_id, term_id)
        cursor.execute(resource_term_insert_query, resource_term_data)

def insert_script_details(cursor, resource_id, scripts_by_id):
    for script_id, script_data in scripts_by_id.items():
        # Insert into Scripts table
        script_insert_query = """
            INSERT INTO Scripts (id, resource_id, operation, approved, user_id,created_at,updated_at)
            VALUES (%s, %s, %s, %s, %s,NOW(),NOW())
        """
        script_data_tuple = (
            script_id,
            resource_id,
            script_data['operation'],
            script_data['approved'],
            script_data['user_id']
        )
        cursor.execute(script_insert_query, script_data_tuple)
        script_id = cursor.lastrowid  # Assuming Scripts.id is auto-incremented

        # Insert into script_terms (for each taxonomy slug and term title combination)
        for tax_slug, term_titles in script_data.items():
            if tax_slug in ['idiomas_title', 'formato_title', 'modo_utilizacao_title', 'requisitos_tecnicos_title', 'anos_escolaridade_title']:
                taxonomy_id = get_taxonomy_id_for_slug(tax_slug)
                for term_title in term_titles:
                    term_id = get_term_id_for_title(term_title)
                    if term_id is not None:
                        script_term_insert_query = """
                            INSERT INTO script_terms (script_id, term_id)
                            VALUES (%s, %s)
                        """
                        script_term_data = (script_id, term_id)
                        cursor.execute(script_term_insert_query, script_term_data)



def get_recent_approved_resources_with_details(limit=8):
    """Get the most recent approved resources with combined details."""
    recent_resources = get_recent_approved_resources(limit=limit)
    
    if recent_resources:
        for resource in recent_resources:
            resource['combined_details'] = get_combined_details(resource['id'])
    
    return recent_resources




def no_resources(userid):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS resource_count FROM Resources WHERE user_id=%s", (userid,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0


def get_resource_image_url(resource_slug):
    image_extensions = ['png', 'jpg','JPG','PNG']
    directory_path = os.path.join(current_app.root_path, 'static', 'files', 'resources', resource_slug)

    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for ext in image_extensions:
            for filename in os.listdir(directory_path):
                if filename.startswith(resource_slug) and filename.endswith('.' + ext):
                    return url_for('static', filename=f'files/resources/{resource_slug}/{filename}')

    return None  # Return None if no image is found

def get_resource_files(resource_slug):
    file_extensions = ['pdf', 'docx', 'xlsx']  # Add other file extensions as needed
    directory_path = os.path.join(current_app.root_path, 'static', 'files', 'resources', resource_slug)
    files = []

    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for ext in file_extensions:
            for filename in os.listdir(directory_path):
                if filename.startswith(resource_slug) and filename.endswith('.' + ext):
                    file_url = url_for('static', filename=f'files/resources/{resource_slug}/{filename}')
                    files.append(file_url)

    return files  # Return a list of file URLs


def get_taxonomy_id_for_title(title):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        query = "SELECT id FROM Taxonomies WHERE title = %s"
        cursor.execute(query, (title,))
        result = cursor.fetchone()

        if result:
            taxonomy_id = result[0]
            return taxonomy_id
        else:
            print(f"Taxonomy with title '{title}' not found.")
            return None

    except mysql.connector.Error as e:
        print(f"Error retrieving taxonomy id for title '{title}': {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def get_taxonomy_id_for_slug(slug):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        query = "SELECT id FROM Taxonomies WHERE slug = %s"
        cursor.execute(query, (slug,))
        result = cursor.fetchone()

        if result:
            taxonomy_id = result[0]
            return taxonomy_id
        else:
            print(f"Taxonomy with slug '{slug}' not found.")
            return None

    except mysql.connector.Error as e:
        print(f"Error retrieving taxonomy id for slug '{slug}': {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def get_term_id_for_title(term_title):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        query = "SELECT id FROM Terms WHERE title = %s"
        cursor.execute(query, (term_title,))
        result = cursor.fetchone()

        if result:
            term_id = result[0]
            return term_id
        else:
            print(f"Term with title '{term_title}' not found.")
            return None

    except mysql.connector.Error as e:
        print(f"Error retrieving term id for title '{term_title}': {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()



def get_resouce_slug(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT slug FROM Resources WHERE id=%s", (resource_id,))
    slug = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    
    if slug:
        return slug['slug']
    else:
        return None
    
def get_resouce_id(slug):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM Resources WHERE slug=%s", (slug,))
    id = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    
    if id:
        return id['id']
    else:
        return None
    
def generate_slug(title):
    # Remove special characters and convert spaces to dashes
    slug = re.sub(r'[^\w\s-]', '', title.lower().strip())
    slug = re.sub(r'\s+', '-', slug)
    return slug
    
def get_resource_embed(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT embed FROM Resources WHERE id=%s", (resource_id,))
    embed = cursor.fetchone()  # fetchone is used because we expect only one resource with the given id
    cursor.close()
    conn.close()

    if embed:
        return embed['embed']
    else:
        return None
    

def get_resource_link(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT link FROM Resources WHERE id=%s", (resource_id,))
    link = cursor.fetchone()  # fetchone is used because we expect only one resource with the given id
    cursor.close()
    conn.close()

    if link:
        return link['link']
    else:
        return None

def get_propostasOp(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT operation FROM Scripts WHERE resource_id=%s", (resource_id,))
    operations = cursor.fetchall()  # fetchall is used to get all matching records
    cursor.close()
    conn.close()

    if operations:
        return [operation['operation'] for operation in operations]
    else:
        return []

def search_resources(search_term, page, per_page):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT SQL_CALC_FOUND_ROWS * FROM Resources
        WHERE title LIKE %s OR description LIKE %s ORDER BY id DESC
        LIMIT %s OFFSET %s
    """
    search_term = f"%{search_term}%"
    offset = (page - 1) * per_page
    cursor.execute(query, (search_term, search_term, per_page, offset))
    resources = cursor.fetchall()
    cursor.execute("SELECT FOUND_ROWS()")
    total_results = cursor.fetchone()["FOUND_ROWS()"]
    cursor.close()
    conn.close()
    return resources, total_results


def get_current_month_resources():
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        
        # Get the current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # SQL query to select resources created in the current month
        query = """
            SELECT COUNT(*) FROM Resources 
            WHERE YEAR(created_at) = %s AND MONTH(created_at) = %s
        """
        cursor.execute(query, (current_year, current_month))
        resources = cursor.fetchall()
        
        logging.info(f"Retrieved {len(resources)} resources created in the current month.")
        
        return resources
    except Exception as e:
        logging.error(f"Error retrieving resources for the current month: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        

def get_active_month_users():
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        
         # Get the current year and month
        #current_year = datetime.now().year
        current_year = 2024
        #current_month = datetime.now().month
        current_month = 5
        
        
        # SQL query to select count of resources by author created in the current month
        query = """
            SELECT author, COUNT(*) AS resource_count FROM Resources 
            WHERE YEAR(created_at) = %s AND MONTH(created_at) = %s
            GROUP BY author
        """
        cursor.execute(query, (current_year, current_month))
        active_users = cursor.fetchall()
        
        logging.info(f"Retrieved {len(active_users)} active users with resources created in the current month.")
        
        return active_users
    except Exception as e:
        logging.error(f"Error retrieving active users for the current month: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
    


def strip_html_tags(text):
    """Remove HTML tags from a string."""
    if not isinstance(text, str):
        return text
    clean = re.compile(r'<.*?>')
    return re.sub(clean, '', text)

