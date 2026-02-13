-- Create asset_categories table in raja database
-- Run this in pgAdmin Query Tool after selecting 'raja' database

CREATE TABLE IF NOT EXISTS asset_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_asset_categories_name ON asset_categories(name);
CREATE INDEX IF NOT EXISTS idx_asset_categories_code ON asset_categories(code);

-- Insert some sample categories
INSERT INTO asset_categories (name, description, code)
VALUES 
    ('Weapons', 'Military weapons and firearms', 'WPN'),
    ('Vehicles', 'Military vehicles and transport', 'VEH'),
    ('Equipment', 'General military equipment', 'EQP'),
    ('Ammunition', 'Ammunition and explosives', 'AMM'),
    ('Communication', 'Communication devices and systems', 'COM')
ON CONFLICT (name) DO NOTHING;

-- Verify table was created
SELECT * FROM asset_categories ORDER BY id;
