-- CREATE DATABASE DATABASE_NAME
-- USE DATABASE_NAME
  
-- Profile
CREATE TABLE profile(
    id int NOT NULL AUTO_INCREMENT,
    agent VARCHAR(50),
    review VARCHAR(255),
    avg_rating FLOAT(3,2) DEFAULT 0.00,
    view_cars VARCHAR(20) DEFAULT 'yes',
    sell_cars VARCHAR(20) DEFAULT 'yes',
    PRIMARY KEY(id),
    FOREIGN KEY(agent) REFERENCES users(name, profile)
)

-- Review List
CREATE TABLE review_list(
    id int NOT NULL AUTO_INCREMENT,
    agent VARCHAR(255),
    rating float(3,2) DEFAULT 0.00,
    descript VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (agent) REFERENCES users(name)
)

-- Car Brands
CREATE TABLE car_brand(
    id INT AUTO_INCREMENT,
    name VARCHAR(255),
    PRIMARY KEY(id,name)
)

-- Car Model
CREATE TABLE car_model(
    id INT AUTO_INCREMENT,
    name VARCHAR(255),
    year INT,
    make VARCHAR(255),
    brand VARCHAR(255),
    type VARCHAR (255),
    PRIMARY KEY(id),
    FOREIGN KEY(brand) REFERENCES car_brand(name)
)

-- Car Listing
CREATE TABLE car_list(
    id int AUTO_INCREMENT,
    reg_no VARCHAR(40),
    brand VARCHAR(255),
    model VARCHAR(255),
    type VARCHAR(50),
    color VARCHAR(255),
    price FLOAT(15,2) DEFAULT 0.00,
    mileage INT DEFAULT 0,
    descrip VARCHAR(1000),
    sale_status VARCHAR(255),
    viewCount INT DEFAULT 0,
    shortlistCount INT DEFAULT 0,
    email VARCHAR(255),
    PRIMARY KEY (id, reg_no),
    FOREIGN KEY(model) REFERENCES model(name),
    FOREIGN KEY(email) REFERENCES users(email),
    FOREIGN KEY(brand) REFERENCES car_brand(name)
)


