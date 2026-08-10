CREATE TABLE IF NOT EXISTS favorites (
    favorites_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    list_name VARCHAR (60) NOT NULL,
    item_id VARCHAR(255) NOT NULL,
    item_type VARCHAR(60) NOT NULL,
    item_name Varchar(255) NOT NULL,
    CONSTRAINT fk_favorites_users
        FOREIGN KEY (user_id)
        REFERENCES  users(user_id)
);