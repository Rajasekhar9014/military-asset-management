"""
Create all database tables for Military Asset Management System
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text
from app.db.session import engine, Base
from app.models.user import User
from app.models.asset_category import AssetCategory
from app.models.unit import Unit
from app.models.asset import Asset
from app.models.purchase import Purchase
from app.models.transfer import Transfer
from app.models.assignment import Assignment, Expenditure


def create_all_tables():
    """Create all database tables"""
    try:
        print("=" * 70)
        print("CREATING ALL DATABASE TABLES")
        print("=" * 70)
        print()
        
        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ All tables created successfully!")
        print()
        
        # Insert sample units
        print("Inserting sample units...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM units"))
            count = result.scalar()
            
            if count == 0:
                conn.execute(text("""
                    INSERT INTO units (name, code, location, description)
                    VALUES 
                        ('Northern Command', 'NC', 'Delhi', 'Northern military command HQ'),
                        ('Southern Command', 'SC', 'Pune', 'Southern military command HQ'),
                        ('Eastern Command', 'EC', 'Kolkata', 'Eastern military command HQ'),
                        ('Western Command', 'WC', 'Chandigarh', 'Western military command HQ')
                """))
                conn.commit()
                print("✅ Sample units inserted!")
            else:
                print(f"⚠️  Units table already has {count} records")
        
        print()
        print("Verifying tables...")
        with engine.connect() as conn:
            tables = [
                'users', 'asset_categories', 'units', 'assets',
                'purchases', 'transfers', 'assignments', 'expenditures'
            ]
            
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  ✅ {table}: {count} records")
        
        print()
        print("=" * 70)
        print("✅ SUCCESS! All tables created and verified")
        print("=" * 70)
        print()
        print("Database is ready for use!")
        print("Server will auto-reload with new models.")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = create_all_tables()
    if not success:
        sys.exit(1)
