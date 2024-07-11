import mysql.connector
from db_operations.admin import *
from db_operations.resources import *
from db_operations.new_resource import *
from db_operations.apps import *
from db_operations.tools import *
from db_operations.resources_details import *
from db_operations.users_op import *
from db_operations.scripts import *
from db_operations.user import *

# MySQL connection configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passroot',
    'database': 'redav4'
}

try:
    # Attempt to establish a connection to the MySQL database
    connection = mysql.connector.connect(**config)

    if connection.is_connected():
        print("Connected to MySQL database")

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor(dictionary=True)
        
        # Call the function to get combined details
        
        # Example usage of insert_combined_details function

        # Sample data for resource_details
        taxonomy_details = {
            'idiomas_title': 'Portuguese',
            'formato_title': 'PDF',
            'modo_utilizacao_title': 'Online',
            'requisitos_tecnicos_title': 'None',
            'anos_escolaridade_title': '1st Grade',
            'created_at': '2024-07-11 12:00:00'
        }
        
        insert_taxonomy_details(cursor,4027,taxonomy_details)
        # After calling the function, commit the transaction and handle any errors appropriately.
        connection.commit()
        
        

       

        # Print the formatted string
        
    
    # Close the cursor
    cursor.close()

    # Close the database connection
    connection.close()
    print("Connection closed")

except mysql.connector.Error as e:
    # Handle connection errors
    print("Error connecting to MySQL database:", e)
