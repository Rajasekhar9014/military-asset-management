# 🔧 CREATE TABLES - 3 Methods

## Problem
Tables are not appearing in your `kristalball` database.

## ✅ Method 1: Run SQL Script in pgAdmin (EASIEST)

1. Open **pgAdmin**
2. Connect to your PostgreSQL server
3. Right-click on **kristalball** database → **Query Tool**
4. Open the file: **`create_users_table.sql`**
5. Click **Execute** (F5) or the ▶️ button
6. You should see: "Query returned successfully"
7. Refresh Tables: Right-click **Tables** → **Refresh**
8. You'll see the **users** table!

## ✅ Method 2: Run Python Script

Open **Command Prompt** (not PowerShell):

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python create_tables.py
```

You should see:
```
✅ Tables created successfully!
Tables in database:
  • users (11 columns)
```

Then create test user:
```cmd
python create_test_user.py
```

## ✅ Method 3: Run from Python Console

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python
```

Then paste this:
```python
from app.db.session import Base, engine
from app.models.user import User
Base.metadata.create_all(bind=engine)
print("✅ Tables created!")
exit()
```

## 🔍 Verify Tables Were Created

### In pgAdmin:
1. Navigate to: **Servers → PostgreSQL → Databases → kristalball → Schemas → public → Tables**
2. Right-click **Tables** → **Refresh**
3. You should see: **users**

### Using Python:
```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python verify_database.py
```

## 🧪 Test the Table

Run this SQL in pgAdmin Query Tool:

```sql
-- Check if table exists
SELECT * FROM users;

-- Should show the admin user
```

## 🔧 Troubleshooting

**"relation does not exist":**
- Table wasn't created. Try Method 1 (SQL script)

**"permission denied":**
- Make sure you're connected as `postgres` user

**"database does not exist":**
- Make sure `kristalball` database exists
- Create it: `CREATE DATABASE kristalball;`

**Python errors:**
- Make sure you're in the `backend` directory
- Install dependencies: `pip install sqlalchemy psycopg2-binary python-dotenv`

## ✨ Recommended: Use Method 1

**Method 1 (SQL script in pgAdmin) is the most reliable** because:
- You can see exactly what's happening
- No Python dependencies needed
- Direct database access
- Immediate feedback

**File to use**: `create_users_table.sql` (in F-API folder)

Just open it in pgAdmin Query Tool and run it! 🚀
