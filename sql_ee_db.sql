CREATE DATABASE IF NOT EXISTS earthecho_db;

USE earthecho_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) COLLATE utf8_bin UNIQUE NOT NULL,
    phone_num INT(8) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    passwd VARCHAR(255) NOT NULL,
    acc_type VARCHAR(5) NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_user_id INT NOT NULL,
    receiver_user_id INT NOT NULL,
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    username VARCHAR(50) COLLATE utf8_bin,
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

-- DROP DATABASE earthecho_db;

SELECT * FROM users;

/*INSERT INTO users (username, phone_num, email, passwd, acc_type) VALUES 
('Tom', 12345678, 'tom@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'user'),
('Jane', 12345378, 'jane@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'user'),
('Harry', 12325678, 'harry@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'user'),
('Richard', 12345648, 'richard@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'user'),
('Admin', 19045678, 'admin@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'admin')*/