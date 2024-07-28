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

CREATE TABLE IF NOT EXISTS posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    username VARCHAR(50),
    header TEXT NOT NULL,
    body TEXT NOT NULL,
    topic TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username),
	FOREIGN KEY (user_id) REFERENCES users(user_id),
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    review TEXT NOT NULL,
    rating INT NOT NULL,
    post_id INT,
    user_id INT,
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
