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
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # Define the change term
        change = "1º,educação artistica - artes visuais, apropriacao e reflexao,universos visuais,pintura"
        
        # Call the insert_term function
        insert_term(change, cursor)  # Ensure insert_term takes a cursor argument

        # Commit changes
        connection.commit()
        
        # Close the cursor
        cursor.close()

    # Close the database connection
    connection.close()
    print("Connection closed")

except mysql.connector.Error as e:
    # Handle connection errors
    print("Error connecting to MySQL database:", e)
