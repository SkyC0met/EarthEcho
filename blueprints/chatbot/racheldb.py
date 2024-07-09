import mysql.connector


def connect_and_fetch():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='aspjuser',
            password='root',
            port='3306',
            database='aspjdb'
        )

        return connection

        # if connection.is_connected():
            # print("Connected to the database")

            # Create a cursor object
            # cursor = connection.cursor()

            # # Write the query
            # query = "SELECT * FROM users"
            #
            # # Execute the query
            # cursor.execute(query)
            #
            # # Fetch all the rows
            # rows = cursor.fetchall()
            #
            # # Print the data
            # for row in rows:
            #     print(row)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return None # connection failed
    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()
    #         print("Connection closed")


if __name__ == "__main__":
    connect_and_fetch()
