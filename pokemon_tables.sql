CREATE TABLE pokemonType(
    pt_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pt_name VARCHAR(30)
);




CREATE TABLE trainer(
    t_id INT AUTO_INCREMENT PRIMARY KEY,
    t_name VARCHAR(20),
    t_town VARCHAR(20)
);


CREATE TABLE pokemon(
    p_id INT NOT NULL PRIMARY KEY,
    p_name VARCHAR(20),
    p_height FLOAT,
    p_weight FLOAT
);


CREATE TABLE typeOf(
    type_id INT NOT NULL,
    pokemon_id INT NOT NULL,
    FOREIGN KEY(type_id) REFERENCES pokemonType(pt_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(p_id)
);




CREATE TABLE ownedBy(
    trainer_id INT NOT NULL,
    pokemon_id INT NOT NULL,
    FOREIGN KEY(trainer_id) REFERENCES trainer(t_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(p_id)
);
