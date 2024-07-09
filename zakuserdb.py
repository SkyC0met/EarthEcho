import mysql.connector

cnx = mysql.connector.connect(
    user='username',
    password='password',
    host='127.0.0.1',
    database='zakdb'
)

cursor = cnx.cursor()

# Create database and switch to it
cursor.execute("CREATE DATABASE users")
cursor.execute("USE users")

# Create tables
cursor.execute("""
    CREATE TABLE users (
      id INT PRIMARY KEY AUTO_INCREMENT,
      username VARCHAR(255) NOT NULL,
      password VARCHAR(255) NOT NULL,
      email VARCHAR(255) NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE posts (
      id INT PRIMARY KEY AUTO_INCREMENT,
      post_id INT NOT NULL,
      topic VARCHAR(255) NOT NULL,
      header VARCHAR(255) NOT NULL,
      subtext TEXT NOT NULL,
      image VARCHAR(255) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

# Commit and close
cnx.commit()
cnx.close()