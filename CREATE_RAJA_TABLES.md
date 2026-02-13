# 🔧 Create Tables in Raja Database - Manual Steps

## The tables weren't created automatically. Here's how to create them:

### ✅ Method 1: Using pgAdmin (EASIEST & RECOMMENDED)

1. **Open pgAdmin**
2. **Connect to PostgreSQL server**
3. **Right-click on `raja` database** → **Query Tool**
4. **Open the file**: `create_raja_database.sql` (in F-API folder)
5. **Click Execute** (▶️ button or press F5)
6. **You should see**: "Query returned successfully"
7. **Refresh Tables**: Right-click **Tables** → **Refresh**
8. **You'll see**: `users` table!

### ✅ Method 2: Using Command Line

Open Command Prompt and run:

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API

psql -U postgres -d raja -f create_raja_database.sql
```

Enter password when prompted: `1234`

### ✅ Method 3: Copy-Paste SQL

1. Open pgAdmin
2. Right-click `raja` database → Query Tool
3. Copy and paste this SQL:

```sql
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

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

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
```

4. Click Execute (▶️)

## 🔍 Verify Tables Were Created

In pgAdmin:
1. Navigate to: **Databases → raja → Schemas → public → Tables**
2. Right-click **Tables** → **Refresh**
3. You should see: **users**
4. Right-click **users** → **View/Edit Data** → **All Rows**
5. You'll see the admin user!

## ✅ Once Tables Are Created

Restart your server:

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python -m uvicorn app.main:app --reload
```

Then test at: **http://127.0.0.1:8000/docs**

Login: admin / Admin123!

## 🎯 Recommended: Use Method 1 (pgAdmin)

It's the most reliable and you can see exactly what's happening!
