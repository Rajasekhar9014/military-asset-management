"""
Create asset_categories table in the database
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text
from app.db.session import engine
from app.models.asset_category import AssetCategory
from app.db.session import Base


def create_asset_categories_table():
    """Create asset_categories table and add sample data"""
    try:
        print("=" * 60)
        print("CREATING ASSET CATEGORIES TABLE")
        print("=" * 60)
        print()
        
        # Create table
        print("Creating asset_categories table...")
        Base.metadata.create_all(bind=engine, tables=[AssetCategory.__table__])
        print("✅ Table created successfully!")
        print()
        
        # Insert sample data
        print("Inserting sample categories...")
        with engine.connect() as conn:
            # Check if data already exists
            result = conn.execute(text("SELECT COUNT(*) FROM asset_categories"))
            count = result.scalar()
            
            if count > 0:
                print(f"⚠️  Table already has {count} categories")
            else:
                # Insert sample categories
                conn.execute(text("""
                    INSERT INTO asset_categories (name, description, code)
                    VALUES 
                        ('Weapons', 'Military weapons and firearms', 'WPN'),
                        ('Vehicles', 'Military vehicles and transport', 'VEH'),
                        ('Equipment', 'General military equipment', 'EQP'),
                        ('Ammunition', 'Ammunition and explosives', 'AMM'),
                        ('Communication', 'Communication devices and systems', 'COM')
                """))
                conn.commit()
                print("✅ Sample categories inserted!")
            
            print()
            print("Current categories:")
            result = conn.execute(text("SELECT id, name, code, description FROM asset_categories ORDER BY id"))
            categories = result.fetchall()
            
            for cat in categories:
                print(f"  [{cat[0]}] {cat[1]} ({cat[2]}) - {cat[3]}")
        
        print()
        print("=" * 60)
        print("✅ SUCCESS! Asset categories table ready")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Server will auto-reload with new endpoints")
        print("2. Visit http://127.0.0.1:8000/docs")
        print("3. Test the new /api/v1/categories endpoints")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = create_asset_categories_table()
    if not success:
        sys.exit(1)
