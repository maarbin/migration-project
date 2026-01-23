CREATE SCHEMA IF NOT EXISTS crm;

CREATE TABLE IF NOT EXISTS crm.customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    registration_date DATE,
    is_active BOOLEAN DEFAULT FALSE,
    
    -- Audit trial
    _source_system_id INT,
    _migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster searching by email
CREATE INDEX idx_customers_email ON crm.customers(email);