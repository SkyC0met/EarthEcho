import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MYSQL_USER = os.getenv('MYSQL_USER', 'skycomet')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    MYSQL_DB = os.getenv('MYSQL_DB', 'earthecho_db')

    @staticmethod
    def get_db_config():
        return {
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'host': Config.MYSQL_HOST,
            'database': Config.MYSQL_DB
        }
