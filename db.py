import mysql.connector
from flask import current_app

def get_db_connection():
    config = current_app.config
    return mysql.connector.connect(
        user=config['MYSQL_USER'],
        password=config['MYSQL_PASSWORD'],
        host=config['MYSQL_HOST'],
        database=config['MYSQL_DB']
    )
