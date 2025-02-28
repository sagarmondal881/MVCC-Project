CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name TEXT,
    balance INT
);

INSERT INTO accounts (name, balance) VALUES ('Alice', 100);
INSERT INTO accounts (name, balance) VALUES ('Bob', 150);