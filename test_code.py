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
        
        levels_with_titles = {
            1: "1o",
            2: "Desenho",
            3: "apropriacao e reflexao",
            4: "universos visuais",
            5: "pintura"
        }

        insert_term_relationships_and_relations(levels_with_titles)

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
