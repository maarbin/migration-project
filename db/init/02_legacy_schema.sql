CREATE SCHEMA IF NOT EXISTS raw_data;

CREATE TABLE IF NOT EXISTS raw_data.legacy (
    client_id INT PRIMARY KEY,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    registration_date TEXT,
    account_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);