from datetime import datetime
from config import DB_CONFIG  # Import the database configuration
from flask import session
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def get_related_resources(resource_title, limit=4):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)

    try:
        # Split the resource title into keywords
        keywords = resource_title.split()
        
        # Create a LIKE pattern for each keyword
        like_patterns = [f"%{keyword}%" for keyword in keywords]
        
        # Build the query to find related resources
        query = """
            SELECT * FROM Resources
            WHERE  ( 
        """
        
        # Add conditions for each keyword pattern
        query += " OR ".join(["title LIKE %s"] * len(like_patterns))
        
        # Close the WHERE clause and add the conditions and limit
        query += """
            ) AND title != %s AND author IS NOT NULL AND (approvedScientific = 1 AND approvedLinguistic = 1) AND hidden='0' 
            ORDER BY CASE
        """
        
        # Add case for ordering by keyword match count
        for index, keyword in enumerate(keywords):
            query += f" WHEN title LIKE %s THEN {index + 1}"
        
        query += """
            ELSE NULL END
            LIMIT %s
        """
        
        # Prepare the parameters for the query
        query_params = like_patterns + [resource_title] + like_patterns + [limit]
        
        # Execute the query with the patterns and the original title to exclude
        cursor.execute(query, query_params)
        related_resources = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        related_resources = []
    finally:
        cursor.close()
        conn.close()
    
    return related_resources

