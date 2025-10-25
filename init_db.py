#!/usr/bin/env python
"""
Database initialization script
Creates tables and optionally seeds data
"""
import sys
from app import app
from extensions import db
from seed import seed_database

def init_db(seed=False):
    """Initialize the database"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        if seed:
            print("\nSeeding database with initial data...")
            seed_database()
            print("Database seeded successfully!")

if __name__ == '__main__':
    seed = '--seed' in sys.argv or '-s' in sys.argv
    init_db(seed=seed)
    
    if not seed:
        print("\nTip: Run with --seed or -s to populate database with sample data")
        print("Example: python init_db.py --seed")
