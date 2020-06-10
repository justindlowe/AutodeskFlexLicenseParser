CREATE TABLE main (
   username CHAR(100) NOT NULL,
   date CHAR(100) NOT NULL,
   product CHAR(100) NOT NULL,
   PRIMARY KEY (username, date, product)
);