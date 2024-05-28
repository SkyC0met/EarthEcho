import mysql.connector

# Database connection details
db_config = {
    'user': 'myuser',
    'password': 'mypassword',
    'host': '172.27.176.182',  # replace with the server's IP address
    'database': 'mydatabase'
}

try:
    # Establish the connection
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        print("Connected to MySQL database")

        # Your database operations here

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        connection.close()
        print("Connection closed")