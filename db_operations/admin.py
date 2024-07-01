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
    
def get_distinct_values():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT DISTINCT
        IFNULL(NULLIF(term_slug_order_1, ''), 'N/A') AS anos,
        IFNULL(NULLIF(term_slug_order_2, ''), 'N/A') AS disciplinas,
        IFNULL(NULLIF(term_slug_order_3, ''), 'N/A') AS dominios,
        IFNULL(NULLIF(term_slug_order_4, ''), 'N/A') AS subdominios,
        IFNULL(NULLIF(term_slug_order_5, ''), 'N/A') AS conceitos
    FROM (
        SELECT
            GROUP_CONCAT(IF(trs.level = 1, tx.slug, NULL)) AS term_slug_order_1,
            GROUP_CONCAT(IF(trs.level = 2, tx.slug, NULL)) AS term_slug_order_2,
            GROUP_CONCAT(IF(trs.level = 3, tx.slug, NULL)) AS term_slug_order_3,
            GROUP_CONCAT(IF(trs.level = 4, tx.slug, NULL)) AS term_slug_order_4,
            GROUP_CONCAT(IF(trs.level = 5, tx.slug, NULL)) AS term_slug_order_5
        FROM redav3.TermRelationships tr
        INNER JOIN terms_relations trs ON trs.term_relationship_id = tr.id
        INNER JOIN Terms tx ON tx.id = trs.term_id
        GROUP BY tr.id
    ) AS subquery
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    anos = set()
    disciplinas = set()
    dominios = set()
    subdominios = set()
    conceitos = set()
    
    for row in result:
        if row['anos']:
            anos.update(row['anos'].split(','))
        if row['disciplinas']:
            disciplinas.update(row['disciplinas'].split(','))
        if row['dominios']:
            dominios.update(row['dominios'].split(','))
        if row['subdominios']:
            subdominios.update(row['subdominios'].split(','))
        if row['conceitos']:
            conceitos.update(row['conceitos'].split(','))

    return list(anos), list(disciplinas), list(dominios), list(subdominios), list(conceitos)

def taxonomies_relations(filters=None):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT
        tr.id AS id,
        GROUP_CONCAT(IF(trs.level = 1, tx.title, NULL)) AS term_title_order_1,
        GROUP_CONCAT(IF(trs.level = 1, tx.slug, NULL)) AS term_slug_order_1,
        GROUP_CONCAT(IF(trs.level = 2, tx.title, NULL)) AS term_title_order_2,
        GROUP_CONCAT(IF(trs.level = 2, tx.slug, NULL)) AS term_slug_order_2,
        GROUP_CONCAT(IF(trs.level = 3, tx.title, NULL)) AS term_title_order_3,
        GROUP_CONCAT(IF(trs.level = 3, tx.slug, NULL)) AS term_slug_order_3,
        GROUP_CONCAT(IF(trs.level = 4, tx.title, NULL)) AS term_title_order_4,
        GROUP_CONCAT(IF(trs.level = 4, tx.slug, NULL)) AS term_slug_order_4,
        GROUP_CONCAT(IF(trs.level = 5, tx.title, NULL)) AS term_title_order_5,
        GROUP_CONCAT(IF(trs.level = 5, tx.slug, NULL)) AS term_slug_order_5
    FROM redav3.TermRelationships tr
    INNER JOIN terms_relations trs ON trs.term_relationship_id = tr.id
    INNER JOIN Terms tx ON tx.id = trs.term_id
    """
    
    if filters:
        conditions = []
        if filters.get('ano'):
            conditions.append(f"FIND_IN_SET('{filters['ano']}', GROUP_CONCAT(IF(trs.level = 1, tx.slug, NULL)))")
        if filters.get('disciplina'):
            conditions.append(f"FIND_IN_SET('{filters['disciplina']}', GROUP_CONCAT(IF(trs.level = 2, tx.slug, NULL)))")
        if filters.get('dominio'):
            conditions.append(f"FIND_IN_SET('{filters['dominio']}', GROUP_CONCAT(IF(trs.level = 3, tx.slug, NULL)))")
        if filters.get('subdominio'):
            conditions.append(f"FIND_IN_SET('{filters['subdominio']}', GROUP_CONCAT(IF(trs.level = 4, tx.slug, NULL)))")
        if filters.get('conceito'):
            conditions.append(f"FIND_IN_SET('{filters['conceito']}', GROUP_CONCAT(IF(trs.level = 5, tx.slug, NULL)))")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    
    query += " GROUP BY tr.id ORDER BY id"
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    conn.close()
    return result

    
