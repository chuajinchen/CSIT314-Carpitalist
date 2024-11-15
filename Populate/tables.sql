-- Profile
CREATE TABLE profile(
    id int NOT NULL AUTO_INCREMENT,
    profile_type VARCHAR(255),
    search_cars VARCHAR(20) DEFAULT 'yes',
    view_cars VARCHAR(20) DEFAULT 'yes',
    list_cars VARCHAR(20) DEFAULT 'yes',
    descript  VARCHAR(255),
    PRIMARY KEY(id),
    UNIQUE (profile_type)
);
 INSERT INTO profile (profile_type, search_cars, view_cars, list_cars,descript) VALUES ('Buyer','yes', 'yes', 'yes','View cars, view car information, mileage, buy cars');
 INSERT INTO profile (profile_type, search_cars, view_cars, list_cars,descript) VALUES ('Seller','yes', 'yes', 'yes','List cars for sale, manage listings, view buyer requests');
 INSERT INTO profile (profile_type, search_cars, view_cars, list_cars,descript) VALUES ('Used Car Agent','yes', 'yes', 'yes','Assist buyers with car purchases, verify car conditions, liaise with sellers');
 INSERT INTO profile (profile_type, search_cars, view_cars, list_cars,descript) VALUES ('User Admin','yes', 'yes', 'yes','Manage user accounts, access all profiles, add/delete users');

-- Review List
CREATE TABLE review_list(
    id int NOT NULL AUTO_INCREMENT,
    agent_email VARCHAR(255) NOT NULL,
    agent VARCHAR(255) NOT NULL,
    rating float(3,2) DEFAULT 0.00,
    descript VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (agent_email, agent) REFERENCES users(email, name)
);

-- Car Brands
CREATE TABLE car_brand(
    id INT AUTO_INCREMENT,
    name VARCHAR(255),
    PRIMARY KEY(id),
    UNIQUE(name)
);

-- Car Model
CREATE TABLE car_model(
    id INT AUTO_INCREMENT,
    name VARCHAR(255),
    year INT,
    make VARCHAR(255),
    brand VARCHAR(255),
    type VARCHAR (255),
    PRIMARY KEY(id),
    UNIQUE(make),
    FOREIGN KEY(brand) REFERENCES car_brand(name)
);

-- Car Listing
CREATE TABLE car_list(
    id int AUTO_INCREMENT,
    reg_no VARCHAR(40),
    brand VARCHAR(255),
    make_id INT,
    type VARCHAR(50),
    color VARCHAR(255),
    price FLOAT(15,2) DEFAULT 0.00,
    mileage INT DEFAULT 0,
    descrip VARCHAR(1000),
    sale_status VARCHAR(255) DEFAULT 'available',
    viewCount INT DEFAULT 0,
    shortlistCount INT DEFAULT 0,
    agent_email VARCHAR(255),
    seller_email VARCHAR(255),
    PRIMARY KEY (id, reg_no),
    FOREIGN KEY(make_id) REFERENCES car_model(id),
    FOREIGN KEY(agent_email) REFERENCES users(email),
    FOREIGN KEY(seller_email) REFERENCES users(email),
    FOREIGN KEY(brand) REFERENCES car_brand(name)
);

-- Add an index to reg_no to support foreign key references
ALTER TABLE car_list ADD INDEX (reg_no);

-- Now, create the shortlist table
CREATE TABLE shortlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_email VARCHAR(255) NOT NULL,
    reg_no VARCHAR(40) NOT NULL,
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_email) REFERENCES users(email) ON DELETE CASCADE,
    FOREIGN KEY (reg_no) REFERENCES car_list(reg_no) ON DELETE CASCADE
);
