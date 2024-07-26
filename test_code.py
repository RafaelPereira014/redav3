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
        
        
        combined_details = get_combined_details(4017)
        if combined_details:
            resource_details = combined_details
            for script_id, script_data in resource_details.get('scripts_by_id', {}).items():
                print(f"Script ID: {script_id}, Areas Resources: {script_data.get('areas_resources')}")
        else:
            print("No details returned.")

        
        


        # Print the formatted string
        
    
    # Close the cursor
    cursor.close()

    # Close the database connection
    connection.close()
    print("Connection closed")

except mysql.connector.Error as e:
    # Handle connection errors
    print("Error connecting to MySQL database:", e)
