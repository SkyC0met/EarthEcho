import mysql.connector

db = mysql.connector.connect(
  host='127.0.0.1',
  user='skycomet', 
  password='password',
  database='remote_database'
)

mycursor = db.cursor()

# mycursor.execute("CREATE TABLE person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("INSERT INTO person (name, age) VALUES (%s,%s)", ("Joe", 22))
#db.commit()

mycursor.execute("SELECT * FROM person")
for i in mycursor:
  print(i)
