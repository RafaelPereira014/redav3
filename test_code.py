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

        scripts_by_id = {
            5000: {
                'operation': 'Operation details',
                'approved': 0,
                'user_id': 5,
                'anos_resources': ['1st Grade'],
                'areas_resources': ['Math'],
                'dominios_resources': ['Science'],
                'subdominios': ['Physics'],
                'hashtags': ['#Learning']
            }
        }
        
        insert_script_details(cursor,4027,scripts_by_id)
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
