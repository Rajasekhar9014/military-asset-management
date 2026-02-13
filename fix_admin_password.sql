-- Fix admin user password
-- This SQL script will update the admin user's password to a properly hashed bcrypt password

-- First, let's see what we have
SELECT id, username, email, role, LEFT(hashed_password, 50) as password_preview 
FROM users 
WHERE username = 'admin';

-- Update the admin user's password
-- This is a bcrypt hash of "Admin123!"
UPDATE users 
SET hashed_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQC92k3Eq'
WHERE username = 'admin';

-- Verify the update
SELECT id, username, email, role, LEFT(hashed_password, 50) as password_preview 
FROM users 
WHERE username = 'admin';
