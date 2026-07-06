CREATE DATABASE users_registration;

use users_registration;

CREATE TABLE users(
    user_id INT PRIMARY KEY AUTO-AUTO_INCREMENT,
    email Varchar(255) NOT NULL UNIQUE,
    password_hash VARCHAR(60) NOT NULL,
);