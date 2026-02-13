-- Create all tables for Military Asset Management System
-- Run this in pgAdmin Query Tool after selecting 'raja' database

-- 1. Units/Bases table
CREATE TABLE IF NOT EXISTS units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    location VARCHAR(200) NOT NULL,
    commander_id INTEGER,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_units_name ON units(name);
CREATE INDEX IF NOT EXISTS idx_units_code ON units(code);

-- 2. Assets table
CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES asset_categories(id),
    unit_id INTEGER NOT NULL REFERENCES units(id),
    serial_number VARCHAR(100) UNIQUE,
    description TEXT,
    unit_price NUMERIC(15, 2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'AVAILABLE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_assets_name ON assets(name);
CREATE INDEX IF NOT EXISTS idx_assets_category_id ON assets(category_id);
CREATE INDEX IF NOT EXISTS idx_assets_unit_id ON assets(unit_id);
CREATE INDEX IF NOT EXISTS idx_assets_serial_number ON assets(serial_number);
CREATE INDEX IF NOT EXISTS idx_assets_status ON assets(status);

-- 3. Purchases table
CREATE TABLE IF NOT EXISTS purchases (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(id),
    unit_id INTEGER NOT NULL REFERENCES units(id),
    category_id INTEGER NOT NULL REFERENCES asset_categories(id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(15, 2) NOT NULL,
    total_amount NUMERIC(15, 2) NOT NULL,
    purchase_date DATE NOT NULL,
    vendor VARCHAR(200),
    invoice_number VARCHAR(100),
    notes VARCHAR(500),
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_purchases_asset_id ON purchases(asset_id);
CREATE INDEX IF NOT EXISTS idx_purchases_unit_id ON purchases(unit_id);
CREATE INDEX IF NOT EXISTS idx_purchases_category_id ON purchases(category_id);
CREATE INDEX IF NOT EXISTS idx_purchases_date ON purchases(purchase_date);

-- 4. Transfers table
CREATE TABLE IF NOT EXISTS transfers (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(id),
    from_unit_id INTEGER NOT NULL REFERENCES units(id),
    to_unit_id INTEGER NOT NULL REFERENCES units(id),
    quantity INTEGER NOT NULL,
    transfer_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    reason VARCHAR(500),
    notes VARCHAR(500),
    initiated_by INTEGER NOT NULL REFERENCES users(id),
    approved_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_transfers_asset_id ON transfers(asset_id);
CREATE INDEX IF NOT EXISTS idx_transfers_from_unit ON transfers(from_unit_id);
CREATE INDEX IF NOT EXISTS idx_transfers_to_unit ON transfers(to_unit_id);
CREATE INDEX IF NOT EXISTS idx_transfers_date ON transfers(transfer_date);
CREATE INDEX IF NOT EXISTS idx_transfers_status ON transfers(status);

-- 5. Assignments table
CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(id),
    unit_id INTEGER NOT NULL REFERENCES units(id),
    assigned_to VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL,
    assignment_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    purpose VARCHAR(500),
    notes VARCHAR(500),
    assigned_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_assignments_asset_id ON assignments(asset_id);
CREATE INDEX IF NOT EXISTS idx_assignments_unit_id ON assignments(unit_id);
CREATE INDEX IF NOT EXISTS idx_assignments_date ON assignments(assignment_date);
CREATE INDEX IF NOT EXISTS idx_assignments_status ON assignments(status);

-- 6. Expenditures table
CREATE TABLE IF NOT EXISTS expenditures (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(id),
    unit_id INTEGER NOT NULL REFERENCES units(id),
    quantity INTEGER NOT NULL,
    expenditure_date DATE NOT NULL,
    reason VARCHAR(500) NOT NULL,
    activity VARCHAR(200),
    notes VARCHAR(500),
    recorded_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_expenditures_asset_id ON expenditures(asset_id);
CREATE INDEX IF NOT EXISTS idx_expenditures_unit_id ON expenditures(unit_id);
CREATE INDEX IF NOT EXISTS idx_expenditures_date ON expenditures(expenditure_date);

-- Insert sample units
INSERT INTO units (name, code, location, description)
VALUES 
    ('Northern Command', 'NC', 'Delhi', 'Northern military command headquarters'),
    ('Southern Command', 'SC', 'Pune', 'Southern military command headquarters'),
    ('Eastern Command', 'EC', 'Kolkata', 'Eastern military command headquarters'),
    ('Western Command', 'WC', 'Chandigarh', 'Western military command headquarters')
ON CONFLICT (name) DO NOTHING;

-- Verify tables
SELECT 'units' as table_name, COUNT(*) as count FROM units
UNION ALL
SELECT 'assets', COUNT(*) FROM assets
UNION ALL
SELECT 'purchases', COUNT(*) FROM purchases
UNION ALL
SELECT 'transfers', COUNT(*) FROM transfers
UNION ALL
SELECT 'assignments', COUNT(*) FROM assignments
UNION ALL
SELECT 'expenditures', COUNT(*) FROM expenditures;
