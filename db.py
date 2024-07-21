import mysql.connector
from mysql.connector import Error
from flask import current_app

def get_db_connection():
    try:
        config = current_app.config
        connection = mysql.connector.connect(
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            host=config['MYSQL_HOST'],
            database=config['MYSQL_DB']
        )
        if connection.is_connected():
            return connection
        else:
            raise ConnectionError("Failed to connect to the database.")
    except Error as e:
        # Handle specific MySQL errors
        raise ConnectionError(f"Error connecting to the database: {e}")
    except Exception as e:
        # Handle other errors
        raise ConnectionError(f"An unexpected error occurred: {e}")