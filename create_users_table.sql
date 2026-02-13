-- Create users table in kristalball database
-- Run this in pgAdmin Query Tool

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role_id INTEGER NOT NULL DEFAULT 1,
    unit_id INTEGER,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Insert test admin user (password is hashed version of "Admin123!")
-- Hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS6NzHZUu
INSERT INTO users (username, email, password_hash, full_name, role_id, is_active)
VALUES (
    'admin',
    'admin@military.mil',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS6NzHZUu',
    'System Administrator',
    1,
    TRUE
)
ON CONFLICT (username) DO NOTHING;

-- Verify table was created
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- Verify user was created
SELECT id, username, email, full_name, is_active, created_at
FROM users;
