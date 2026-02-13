"""
Quick script to check if models have foreign key constraints
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.models.purchase import Purchase

# Check the unit_id column
for column in Purchase.__table__.columns:
    if column.name == 'unit_id':
        print(f"Column: {column.name}")
        print(f"Type: {column.type}")
        print(f"Nullable: {column.nullable}")
        print(f"Foreign Keys: {list(column.foreign_keys)}")
        
        if column.foreign_keys:
            print("❌ PROBLEM: unit_id still has foreign key constraints!")
            for fk in column.foreign_keys:
                print(f"   Foreign key to: {fk.target_fullname}")
        else:
            print("✅ GOOD: unit_id has NO foreign key constraints")
