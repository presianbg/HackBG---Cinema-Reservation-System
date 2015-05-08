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

INSERT INTO Movies(name, rating)
VALUES ("The Hunger Games: Catching Fire", 7.9),
       ("Wreck-It Ralph", 7.8),
       ("Her", 8.3);

INSERT INTO Projections(movie_id, type, projection_date, projection_time)
VALUES(1, "3D", "2014-04-01", "19:10"),
      (1, "2D", "2014-04-01", "19:30"),
      (2, "3D", "2014-04-01", "22:00"),
      (2, "2D", "2014-04-01", "22:30"),
      (3, "3D", "2014-04-01", "14:00");
