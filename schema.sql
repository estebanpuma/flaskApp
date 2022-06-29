DROP TABLE IF EXISTS voltajes;

CREATE TABLE voltajes(
    hora TEXT PRIMARY KEY,
    v1 INTEGER NOT NULL,
    v2 INTEGER NOT NULL,
    v3 INTEGER NOT NULL

);

CREATE TABLE refrigeracion(
    hora TEXT PRIMARY KEY,
    filtroU1 FLOAT NOT NULL,
    filtroU2 FLOAT NOT NULL,
    flujometroU1 FLOAT NOT NULL,
    flujometroU2 FLOAT NOT NULL,
    intercambiadorU1 FLOAT NOT NULL,
    intercambiadorU2 FLOAT NOT NULL
);