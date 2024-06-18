import mysql.connector
from db_operations.admin import *
from db_operations.resources import *
from db_operations.new_resource import *
from db_operations.apps import *
from db_operations.tools import *

# MySQL connection configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passroot',
    'database': 'redav3'
}

try:
    # Attempt to establish a connection to the MySQL database
    connection = mysql.connector.connect(**config)

    if connection.is_connected():
        print("Connected to MySQL database")

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()
        
        change = get_all_details_resource('3900')
        #name = get_username(9)
        change_str = str(change)

        # Replace commas with newlines
        formatted_change = change_str.replace(',', ',\n')

        # Print the formatted string
        print(formatted_change)
    # Close the database connection
    connection.close()
    print("Connection closed")

except mysql.connector.Error as e:
    # Handle connection errors
    print("Error connecting to MySQL database:", e)