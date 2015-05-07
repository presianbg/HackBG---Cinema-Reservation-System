PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS Movies;

CREATE TABLE IF NOT EXISTS Movies(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    rating REAL
    );


DROP TABLE IF EXISTS Projections;

CREATE TABLE IF NOT EXISTS Projections(
    id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    type TEXT,
    projection_date DATE,
    projection_time TIME,
    FOREIGN KEY(movie_id) REFERENCES Movies(id)
    );

DROP TABLE IF EXISTS Reservations;

CREATE TABLE IF NOT EXISTS Reservations(
    id INTEGER PRIMARY KEY,
    username TEXT,
    projection_id INTEGER,
    row INTEGER,
    col INTEGER,
   FOREIGN KEY(projection_id) REFERENCES Projections(id)
    );
