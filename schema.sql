-- Demo schema for the shop API.
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
);

INSERT INTO users (name, email, password_hash) VALUES
    ('Alice', 'alice@example.com', '5f4dcc3b5aa765d61d8327deb882cf99'),
    ('Bob', 'bob@example.com', '5f4dcc3b5aa765d61d8327deb882cf99');

INSERT INTO orders (customer, total, status) VALUES
    ('Alice', 42.5, 'paid'),
    ('Bob', 13.0, 'pending');
