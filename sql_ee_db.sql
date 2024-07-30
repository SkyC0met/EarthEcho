-- DROP DATABASE IF EXISTS earthecho_db;

CREATE DATABASE IF NOT EXISTS earthecho_db;

USE earthecho_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) COLLATE utf8_bin UNIQUE NOT NULL,
    phone_num VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    passwd VARCHAR(255) NOT NULL,
    acc_type VARCHAR(5) NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_user_id INT NOT NULL,
    receiver_user_id INT NOT NULL,
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS points_shop (
    reward_id INT AUTO_INCREMENT PRIMARY KEY,
    reward_name VARCHAR(100) NOT NULL,
    reward TEXT NOT NULL,
    reward_desc TEXT NOT NULL,
    points_required INT NOT NULL,
    valid_until TEXT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    points_type VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS user_redemption (
    redemption_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    reward_id INT NOT NULL,
    redemption_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reward_id) REFERENCES points_shop(reward_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_points (
    user_id INT PRIMARY KEY,
    points_balance INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sky_posts_to_test_fav (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    header TEXT NOT NULL,
    body TEXT NOT NULL,
    topic TEXT NOT NULL,
    image_path VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_favourites (
    favourite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
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

-- Create the review table without foreign keys
CREATE TABLE IF NOT EXISTS review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    review TEXT NOT NULL,
    rating INT NOT NULL,
    post_id INT,
    user_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the unban_requests table
CREATE TABLE IF NOT EXISTS unban_requests (
    username VARCHAR(255) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    request TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/*INSERT INTO review (review_id, review, rating, post_id, user_id, timestamp) VALUES
('77', 'well written', '5', '1', '3', '2024-07-30 10:12:23');

INSERT INTO users (username, phone_num, email, passwd, acc_type) VALUES
('Tom', '12345678', 'tom@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'user'),
('Jane', '12345378', 'jane@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'user'),
('Harry', '12325678', 'harry@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'user'),
('Richard', '12345648', 'richard@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'user'),
('Admin', '19045678', 'admin@gmail.com', 'scrypt:32768:8:1$GB2hqTmVOBZBXfGO$dcdfa47ebd93848e85079cd0eec0d20b55c48ae9f54cafc21f2085ef5acea53d830148710c17b95fd7003acb524074357c9c5b9ede32e970bdb6abe7f1f04774', 'admin');

INSERT INTO points_shop (reward_name, reward, reward_desc, points_required, valid_until, image_path, points_type) VALUES
('Bistro Bella', '15% OFF total bill', 'Bistro Bella is a cozy, rustic bistro serving classic French cuisine with a modern twist, perfect for intimate dinners and casual lunches.', 1500, '31 Dec 2024', 'images/food/food1.jpg', 'food'),
('The Culinary Delight', '10% OFF main course', 'A fusion restaurant offering a blend of Asian and European cuisines, known for its innovative dishes and elegant ambiance.', 1000, '31 Dec 2024', 'images/food/food2.jpg', 'food'),
('Veggie Haven', 'Free dessert with any entrée', 'A vegetarian and vegan restaurant offering a wide variety of flavorful and healthy dishes made from locally sourced ingredients.', 2000, '31 Dec 2024', 'images/food/food3.jpg', 'food'),
('Sushi House', '10% OFF sushi rolls', 'A modern Japanese restaurant known for its fresh sushi, sashimi, and creative rolls, offering an authentic taste of Japan in a chic setting.', 1000, '31 Dec 2024', 'images/food/food4.jpg', 'food'),
('Ocean Breeze Bistro', '20% OFF any seafood entrée', 'A coastal-themed bistro offering a variety of fresh seafood dishes, artisanal cocktails, and a relaxed atmosphere with ocean views.', 2000, '31 Dec 2024', 'images/food/food5.jpg', 'food'),
('Italia Trattoria', 'Free dessert with any pasta dish', 'A charming Italian trattoria serving traditional Italian dishes, including handmade pasta, wood-fired pizzas, and classic desserts.', 1500, '31 Dec 2024', 'images/food/food6.jpg', 'food'),
('Bracafe', 'Buy one coffee, get one free', 'A trendy café offering a wide selection of specialty coffees, freshly baked pastries, and light meals, perfect for a casual hangout or a quick bite.', 500, '31 Dec 2024', 'images/food/food7.jpg', 'food'),
('The Mug House', '15% OFF first round of drinks', 'A charming pub-style restaurant serving hearty comfort food, craft beers, and signature cocktails, ideal for a relaxed and cozy dining experience.', 1500, '31 Dec 2024', 'images/food/food8.jpg', 'food'),
('Hugo Boss', '10% off storewide', 'A renowned global fashion brand offering high-quality, sophisticated clothing, accessories, and fragrances for men and women, known for its sleek and contemporary designs.', 1000, '31 Dec 2024', 'images/fashion/fashion1.jpg', 'fashion'),
('Urban Chic', '15% off on all jackets and outerwear', 'A trendy fashion store featuring the latest in streetwear and casual fashion for both men and women, perfect for the urban lifestyle.', 1500, '31 Dec 2024', 'images/fashion/fashion2.jpg', 'fashion'),
('Vintage Vogue', 'Buy one, get one 50% off on all vintage items', 'A unique shop specializing in vintage and retro fashion, offering a variety of clothing, shoes, and accessories from past decades.', 500, '31 Dec 2024', 'images/fashion/fashion3.jpg', 'fashion'),
('Kujten', '15% off all cashmere items', 'A luxury cashmere brand providing a range of stylish and comfortable cashmere clothing and accessories, blending French elegance with exceptional quality.', 1500, '31 Dec 2024', 'images/fashion/fashion4.jpg', 'fashion'),
('Les Basics', 'Buy two, get one free on all basics', 'A minimalist fashion store focusing on essential wardrobe pieces with clean lines and timeless appeal, offering high-quality basics for everyday wear.', 500, '31 Dec 2024', 'images/fashion/fashion5.jpg', 'fashion'),
('EcoStyle', '20% off your first purchase', 'A sustainable fashion store dedicated to eco-friendly and ethically made clothing, offering stylish options that are kind to the planet.', 2000, '31 Dec 2024', 'images/fashion/fashion6.jpg', 'fashion'),
('Openmind', '20% off your first purchase', 'An innovative fashion store featuring contemporary designs and sustainable materials, catering to the modern, conscious consumer who values style and ethics.', 1000, '31 Dec 2024', 'images/fashion/fashion7.jpg', 'fashion'),
('Boho Bliss', 'Buy one, get one 50% off on all dresses', 'A bohemian-inspired fashion shop featuring a vibrant selection of flowy dresses, artisanal jewelry, and eclectic accessories for free-spirited individuals.', 500, '31 Dec 2024', 'images/fashion/fashion8.jpg', 'fashion');

INSERT INTO user_points (user_id, points_balance) VALUES
('2', '2000'),
('4', '7000');

INSERT INTO user_redemption (user_id, reward_id) VALUES
('2', '3'),
('2', '7'),
('4', '8');

INSERT INTO sky_posts_to_test_fav (user_id, header, body, topic, image_path) VALUES
(1, 'Embracing Sustainability: A Journey Towards a Greener Future', 'In an age where climate change and environmental degradation are becoming increasingly urgent issues, sustainability is more than just a buzzword;', 'Sustainability', 'images/sky/blogpost1.jpg'),
(1, 'Post 2', 'This is the body of the post.', 'Technology', 'images/fashion/fashion7.jpg'),
(1, 'Post 3', 'This is the body of the post.', 'Technology', 'images/fashion/fashion6.jpg');
*/

SELECT * FROM unban_requests;

/*SELECT ur.user_id, ur.reward_id, ur.redemption_date, ps.reward_name, ps.reward, ps.reward_desc, ps.valid_until, ps.image_path
FROM user_redemption ur
INNER JOIN points_shop ps ON ur.reward_id = ps.reward_id
WHERE ur.user_id = 2;

SELECT uf.user_id, uf.post_id, sp.header, sp.body, sp.image_path
FROM user_favourites uf
INNER JOIN sky_posts_to_test_fav sp ON uf.post_id = sp.post_id
WHERE uf.user_id = 2;
*/
