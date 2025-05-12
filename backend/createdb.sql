CREATE TABLE user(
    username VARCHAR(256),
    password VARCHAR(60) NOT NULL,
    bio VARCHAR(256),
    profile_picture BLOB,
    PRIMARY KEY(username)
);

CREATE TABLE follow(
    username_follower VARCHAR(256) NOT NULL,
    username_followee VARCHAR(256) NOT NULL,
    PRIMARY KEY(username_follower, username_followee),
    FOREIGN KEY(username_follower) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(username_followee) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE recipe(
    recipe_id INTEGER AUTO_INCREMENT,
    author_username VARCHAR(256) NOT NULL,
    publish_date DATE NOT NULL,
    title VARCHAR(60),
    short_description VARCHAR(256),
    steps VARCHAR(1000),
    time INTEGER NOT NULL,
    servings INTEGER NOT NULL,
    sustainability_rating DOUBLE,
    average_rating DOUBLE,
    PRIMARY KEY(recipe_id),
    FOREIGN KEY(author_username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE photo(
    photo_id INTEGER AUTO_INCREMENT,
    photo MEDIUMBLOB NOT NULL,
    recipe_id INTEGER NOT NULL,
    PRIMARY KEY(photo_id),
    FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE rate(
    recipe_id INTEGER,
    username VARCHAR(256),
    value INTEGER NOT NULL,
    PRIMARY KEY(recipe_id, username),
    FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT rating_range CHECK (value>=1 and value<=10)
);

CREATE TABLE likes(
    recipe_id INTEGER,
    username VARCHAR(256),
    PRIMARY KEY(recipe_id, username),
    FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE comment(
    recipe_id INTEGER,
    username VARCHAR(256),
    publish_date DATETIME NOT NULL,
    content VARCHAR(256),
    PRIMARY KEY(recipe_id, username, content),
    FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE bookmark(
    recipe_id INTEGER,
    username VARCHAR(256),
    PRIMARY KEY(recipe_id, username),
    FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ingredient(
    ingredient_name VARCHAR(256),
    sustainability_score DOUBLE,
    PRIMARY KEY(ingredient_name)
);

CREATE TABLE contains_ingredient(
    recipe_id INTEGER,
    ingredient_name VARCHAR(256),
    amount FLOAT,
    weight ENUM('g','kg','lb','oz','l', 'ml', 'tbsp', 'tsp', 'cup', 'pt', 'qt', 'gal', 'floz', 'qty'),
    PRIMARY KEY(recipe_id, ingredient_name),
    FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(ingredient_name) REFERENCES ingredient(ingredient_name) ON UPDATE CASCADE ON DELETE CASCADE
);

delimiter //
CREATE TRIGGER update_average_rating_after_insert_rate AFTER INSERT ON rate
FOR EACH ROW
BEGIN
    DECLARE new_average DOUBLE;

    SELECT AVG(value)
    INTO new_average
    FROM rate
    WHERE recipe_id = NEW.recipe_id;

    UPDATE recipe
    SET average_rating = new_average
    WHERE recipe_id = NEW.recipe_id;
END; //

delimiter //
CREATE TRIGGER update_average_rating_after_delete AFTER DELETE ON rate
FOR EACH ROW
BEGIN
    DECLARE new_average DOUBLE;
    INTO new_average
    FROM rate
    WHERE recipe_id = OLD.recipe_id;

    UPDATE recipe
    SET average_rating = new_average
    WHERE recipe_id = OLD.recipe_id;
END; //

ALTER TABLE recipe
ADD FULLTEXT(title, short_description, steps);