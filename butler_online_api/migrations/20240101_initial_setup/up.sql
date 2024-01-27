CREATE TABLE einzelbuchungen (
    `id` VARCHAR(36) NOT NULL,
    `name` VARCHAR(90) NOT NULL,
    `kategorie` VARCHAR(60) NOT NULL,
    `wert` DECIMAL(10,2) NOT NULL,
    `datum` DATE NOT NULL,
    `user` VARCHAR(60) NOT NULL,
    CONSTRAINT `einzelbuchungen_pk` PRIMARY KEY (id)
);

CREATE TABLE gemeinsame_buchungen (
    `id` VARCHAR(36) NOT NULL,
    `name` VARCHAR(90) NOT NULL,
    `kategorie` VARCHAR(60) NOT NULL,
    `wert` DECIMAL(10,2) NOT NULL,
    `datum` DATE NOT NULL,
    `user` VARCHAR(60) NOT NULL,
    `zielperson` VARCHAR(60) NOT NULL,
    CONSTRAINT `gemeinsame_buchungen_pk` PRIMARY KEY (id)
);

CREATE TABLE kategorien (
    `id` VARCHAR(36) NOT NULL,
    `name` VARCHAR(60) NOT NULL,
    `user` VARCHAR(60) NOT NULL,
    CONSTRAINT `kategorien_pk` PRIMARY KEY (id)
);

CREATE TABLE partner (
    `zielperson` VARCHAR(60) NOT NULL,
    `user` VARCHAR(60) NOT NULL,
    CONSTRAINT `partner_pk` PRIMARY KEY (user)
);

