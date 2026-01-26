"""
Initialize database - create all tables
Run: python scripts/init_db.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Member, Drug, Pharmacy, Claim, Formulary

def init_database():
    print("Initializing database...")
    
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ All tables created successfully!")
        
        # Print table names
        print("\nCreated tables:")
        for table in db.metadata.sorted_tables:
            print(f"  - {table.name}")


if __name__ == '__main__':
    init_database()