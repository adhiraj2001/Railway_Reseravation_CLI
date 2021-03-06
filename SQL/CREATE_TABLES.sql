-- Create Database
DROP DATABASE IF EXISTS railway;

CREATE DATABASE railway;
USE railway;

-- LEVEL 1
-- Tables and References

-- Creating tables
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  user_id int AUTO_INCREMENT PRIMARY KEY,
  password varchar(20)
);


DROP TABLE IF EXISTS passenger;

CREATE TABLE passenger (
  passenger_id int AUTO_INCREMENT PRIMARY KEY,
  name varchar(20) NOT NULL,
  dob date,
  gender varchar(20)
  -- derived attributes not shown
);


DROP TABLE IF EXISTS station;

CREATE TABLE station (
  station_id int AUTO_INCREMENT PRIMARY KEY,
  name varchar(20) NOT NULL UNIQUE,
  
  -- Composite
  street varchar(20),
  city varchar(20),
  state varchar(20)
);


DROP TABLE IF EXISTS ticket;

CREATE TABLE ticket (
  ticket_id int AUTO_INCREMENT PRIMARY KEY,
  date date NOT NULL,
  status boolean DEFAULT 0,

  source int NOT NULL,
  destination int NOT NULL,

  FOREIGN KEY (source) REFERENCES station(station_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    FOREIGN KEY (destination) REFERENCES station(station_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


DROP TABLE IF EXISTS train;

CREATE TABLE train (
  train_id int AUTO_INCREMENT PRIMARY KEY,
  name varchar(20) NOT NULL UNIQUE,

  total_seats int DEFAULT 100,
  price int DEFAULT 1000,

  starts_at int NOT NULL,
  ends_at int NOT NULL,

  FOREIGN KEY (starts_at) REFERENCES station(station_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  FOREIGN KEY (ends_at) REFERENCES station(station_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- LEVEL 2
-- Adding column settings

-- multivalued attributes

DROP TABLE IF EXISTS passenger_contact;

CREATE TABLE passenger_contact (
  passenger_id int NOT NULL,
  mobile_no int,

  FOREIGN KEY (passenger_id) REFERENCES passenger(passenger_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE -- inline relationship (many-to-one)
);


DROP TABLE IF EXISTS passenger_address;

CREATE TABLE passenger_address (
  
  passenger_id int NOT NULL,
  
  -- Composite attributes represented as their atomic attributes
  street varchar(20),
  city varchar(20),
  state varchar(20),

  FOREIGN KEY (passenger_id) REFERENCES passenger(passenger_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE -- inline relationship (many-to-one)
);


DROP TABLE IF EXISTS train_status;

CREATE TABLE train_status (
  train_id int NOT NULL,

  date date NOT NULL,
  booked_seats int DEFAULT 0,

  PRIMARY KEY (train_id, date),
  
  FOREIGN KEY  (train_id) REFERENCES train(train_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


DROP TABLE IF EXISTS route;

CREATE TABLE route (
  stop_no int NOT NULL,
  train_id int NOT NULL,
  station_id int NOT NULL,

  PRIMARY KEY (stop_no, train_id),
  
  FOREIGN KEY (train_id) REFERENCES train(train_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  FOREIGN KEY (station_id) REFERENCES station(station_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Level 3 
-- relationships

DROP TABLE IF EXISTS books;

CREATE TABLE books (
  user_id int,
  passenger_id int,
  ticket_id int UNIQUE,
  
  -- train status primary key
  train_id int,
  date date,

  FOREIGN KEY (user_id) REFERENCES user(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  FOREIGN KEY (passenger_id) REFERENCES passenger(passenger_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  
  FOREIGN KEY (train_id, date) REFERENCES train_status(train_id, date)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- Insert Queries

INSERT INTO user (password)
VALUES 
('ab'), 
('bc'),
('cd');

INSERT INTO passenger (name, dob, gender)
VALUES
('sukhjinder','2003-02-22','MALE'),
('pranjal','2002-03-17','MALE'),
('adhiraj','2001-01-01','MALE'), -- to be checked
('kohli','2010-01-30','MALE'),
('dhoni','2011-04-22','MALE'),
('pvsindhu','2016-06-01','FEMALE');

INSERT INTO station (name, street, city, state)
VALUES 
('chandigarh','abc','chandigarh','Punjab'), -- 1
('Abohar','bcd','Abohar','AP'), -- 2
('Abu','cde','Abu','HP'), -- 3
('Achalda','def','Achalda','UP'), -- 3 
('Achhnera','efg','Achhnera','MP'), -- 4
('Abhaipur','fgh','Abhaipur','UK'), -- 5
('Adavali','ijk','Adavali','Delhi'); -- 6

INSERT INTO train (name, total_seats, price, starts_at, ends_at)
VALUES 
('t1',50,100,1,2), 
('t2',51,101,1,3),
('t3',52,102,2,4),
('t4',53,103,2,5),
('t5',54,104,3,6),
('t6',55,105,3,7);

INSERT INTO passenger_contact (passenger_id, mobile_no)
VALUES
(1,1234567890),
(2,1234567891),
(3,1234567892),
(4,1234567893),
(5,1234567894),
(6,1234567895),
(5,1234567896),
(6,1234567897),
(1,1234567898);

INSERT INTO passenger_address (passenger_id, street, city, state)
VALUES
(1,'abc','chandigarh','Punjab'),
(2,'bcd','Abohar','AP'),
(3,'cde','Abu','HP'),
(4,'def','Achalda','UP'),
(5,'efg','Achhnera','MP'),
(6,'fgh','Abhaipur','UK');

INSERT INTO train_status (train_id, date, booked_seats)
VALUES
(1,'2021-10-01',40), 
(2,'2021-10-02',41),
(3,'2021-10-03',42),
(4,'2021-10-04',43),
(5,'2021-10-05',44),
(6,'2021-10-01',45),
(1,'2021-11-01',46),
(2,'2021-10-01',47),
(3,'2021-10-06',48); 

INSERT INTO route (train_id, stop_no, station_id)
VALUES
(1,1,1),  
(1,2,5), 
(1,3,3),
(2,1,1), 
(2,2,2), 
(2,3,5),
(2,4,4),
(3,1,1), 
(3,2,5), 
(3,3,3),
(3,4,6),
(4,1,1), 
(4,2,2), 
(4,3,3),
(4,4,4),
(4,5,7),
(5,1,1), 
(5,2,6), 
(5,3,5),
(6,1,5), 
(6,2,7), 
(6,3,3);


-- SELECT * from train_status
-- WHERE train_id IN (SELECT (A.train_id) FROM train as A
--     WHERE (A.starts_at = 1 AND (A.ends_at = 4 OR 4 IN (SELECT B.station_id FROM route AS B WHERE B.train_id = A.train_id)))
--     OR (A.ends_at = 4 AND 1 in (SELECT C.station_id FROM route as C WHERE C.train_id = A.train_id))
--     OR ((SELECT (D.stop_no) FROM route AS D WHERE D.train_id = A.train_id AND D.station_id = 1) < ANY (SELECT (E.stop_no) FROM route AS E WHERE E.train_id = A.train_id AND E.station_id = 4)));

-- SELECT (A.train_id) FROM train as A
--     WHERE (A.starts_at = 1 AND (A.ends_at = 4 OR 4 IN (SELECT B.station_id FROM route AS B WHERE B.train_id = A.train_id)))
--     OR (A.ends_at = 4 AND 1 in (SELECT C.station_id FROM route as C WHERE C.train_id = A.train_id))
--     OR ((SELECT (D.stop_no) FROM route AS D WHERE D.train_id = A.train_id AND D.station_id = 1) < ANY (SELECT (E.stop_no) FROM route AS E WHERE E.train_id = A.train_id AND E.station_id = 4));


-- UPDATE ticket SET status = 1
-- WHERE ticket_id IN 
-- (SELECT ticket_id FROM books AS B WHERE user_id = %s AND 
-- ((SELECT booked_seats FROM train_status AS C WHERE C.train_id = B.train_id AND C.date = B.date) <= (SELECT total_seats FROM train AS D WHERE D.traid_id = B.train_id)));

-- SELECT SUM(B.price) AS total_costs FROM
-- (SELECT (train_id) FROM books WHERE user_id = %s) AS A
-- INNER JOIN
-- (SELECT (train_id, price) FROM train) AS B
-- ON A.train_id = B.train_id; 


-- INSERT INTO station (name)
-- VALUES
-- ('a'),
-- ('b'),
-- ('c'),
-- ('d'),
-- ('e'),
-- ('f'),
-- ('g'),
-- ('h');

-- INSERT INTO train (name, starts_at, ends_at)
-- VALUES
-- ('A', 1, 5),
-- ('B', 2, 4),
-- ('D', 7, 1),
-- ('C', 8, 1);

-- INSERT INTO route (stop_no, train_id, station_id)
-- VALUES
-- (1, 1, 2),
-- (2, 1, 3),

-- (1, 2, 3),

-- (1, 3, 4),
-- (2, 3, 3),
-- (3, 3, 2),

-- (1, 4, 2),
-- (2, 4, 4),
-- (3, 4, 3),
-- (4, 4, 7);

-- INSERT INTO route (stop_no, train_id, station_id)
-- VALUES
-- (3, 1, 4);