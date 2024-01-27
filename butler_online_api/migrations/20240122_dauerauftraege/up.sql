
CREATE TABLE dauerauftraege (
    `id` VARCHAR(36) NOT NULL,
    `name` VARCHAR(90) NOT NULL,
    `start_datum` DATE NOT NULL,
    `ende_datum` DATE NOT NULL,
    `kategorie` VARCHAR(60) NOT NULL,
    `wert` DECIMAL(10,2) NOT NULL,
    `user` VARCHAR(60) NOT NULL,
    `rhythmus` VARCHAR(30) NOT NULL,
    `letzte_ausfuehrung` DATE,
    CONSTRAINT `dauerauftraege_pk` PRIMARY KEY (id)
);


CREATE TABLE gemeinsame_dauerauftraege (
    `id` VARCHAR(36) NOT NULL,
    `name` VARCHAR(90) NOT NULL,
    `start_datum` DATE NOT NULL,
    `ende_datum` DATE NOT NULL,
    `kategorie` VARCHAR(60) NOT NULL,
    `wert` DECIMAL(10,2) NOT NULL,
    `user` VARCHAR(60) NOT NULL,
    `rhythmus` VARCHAR(30) NOT NULL,
    `letzte_ausfuehrung` DATE,
    `zielperson` VARCHAR(60) NOT NULL,
    CONSTRAINT `dauerauftraege_pk` PRIMARY KEY (id)
);
