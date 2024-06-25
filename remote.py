import mysql.connector

db = mysql.connector.connect(
  host='127.0.0.1',
  user='skycomet', 
  password='password',
  database='earthecho'
)

mycursor = db.cursor()

mycursor.execute("""
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    phone_num VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    passwd VARCHAR(255) NOT NULL,
    acc_type VARCHAR(20) NOT NULL
)
""")

mycursor.execute("""
CREATE TABLE posts (
    post_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    header VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    topic VARCHAR(100) NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

mycursor.execute("""
CREATE TABLE reviews_and_ratings (
    review TEXT NOT NULL,
    rating INT NOT NULL,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

mycursor.execute("""
CREATE TABLE unban_requests (
    reqId INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    reason TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

mycursor.execute("""
CREATE TABLE point_shop (
    user_id INT NOT NULL,
    no_of_points INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

mycursor.execute("""
CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    sender VARCHAR(50),
    receiver VARCHAR(50),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")



# mycursor.execute("INSERT INTO person (name, age) VALUES (%s,%s)", ("Joe", 22))
#db.commit()

"""mycursor.execute("SELECT * FROM person")
for i in mycursor:
  print(i)
"""