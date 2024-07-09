CREATE DATABASE IF NOT EXISTS earthecho_db;

USE earthecho_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    phone_num INT(8) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    passwd VARCHAR(255) NOT NULL,
    acc_type VARCHAR(5) NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_user_id INT NOT NULL,
    sender VARCHAR(50),
    receiver VARCHAR(50),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INSERT INTO messages (sender_user_id, sender, receiver, message) 
-- VALUES (2, 'Tom', 'Customer', 'Hello Bob, how are you?');

-- SHOW TABLES;

-- DELETE FROM messages WHERE sender_user_id = 1
SELECT * FROM users;

