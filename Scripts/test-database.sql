--
--  test-database.sql
--  Progetto di Distributed Systems and Big Data
--  Anno Accademico 2024-25
--  (C) 2024 Luca Montera, Alessio Giordano
--
--  Created by Alessio Giordano on 25/11/24.
--

CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY,
    ticker VARCHAR(255)
);
CREATE TABLE stock (
    ticker VARCHAR(255) PRIMARY KEY,
    value DECIMAL(10, 2),
    timestamp DATETIME
);
INSERT INTO users (email, ticker) VALUES
('user1@example.com', 'AAPL'),
('user2@example.com', 'GOOGL'),
('user3@example.com', 'MSFT'),
('user4@example.com', 'AMZN'),
('user5@example.com', 'TSLA');
INSERT INTO stock (ticker, value, timestamp) VALUES
('AAPL', 150.25, '2023-10-01 10:00:00'),
('GOOGL', 2750.75, '2023-10-01 10:05:00'),
('MSFT', 300.50, '2023-10-01 10:10:00'),
('AMZN', 3300.00, '2023-10-01 10:15:00'),
('TSLA', 220.75, '2023-10-01 10:20:00');
SELECT * from users;
INSERT INTO users (email, ticker) VALUES
('user6@example.com', 'AAPL'),
('user7@example.com', 'GOOGL');
SELECT DISTINCT ticker from users;