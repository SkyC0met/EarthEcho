import mysql.connector

def connect_and_fetch():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host='127.0.0.1',       # e.g., 'localhost' or '127.0.0.1'
            user='skycomet',   # your MySQL username
            password='password', # your MySQL password
            database='earthecho'    # name of the database
        )

        if connection.is_connected():
            print("Connected to the database")

            # Create a cursor object
            cursor = connection.cursor()

            # Write the query
            query = "SELECT * FROM user"

            # Execute the query
            cursor.execute(query)

            # Fetch all the rows
            rows = cursor.fetchall()

            # Print the data
            for row in rows:
                print(row)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

if __name__ == "__main__":
    connect_and_fetch()
