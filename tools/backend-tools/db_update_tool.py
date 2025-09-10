#!/usr/bin/env python3
"""
Database Update Tool
Simple tool for running database schema updates and migrations
"""

import os
import psycopg2
from urllib.parse import urlparse
import sys

class DatabaseUpdater:
    def __init__(self, database_url: str = None):
        if database_url:
            self.database_url = database_url
        else:
            # Try to load from environment or .env file
            self.database_url = self._get_database_url()
        
        if not self.database_url:
            raise ValueError("No database URL provided. Set DATABASE_URL environment variable or provide in constructor.")
    
    def _get_database_url(self):
        """Get database URL from environment or .env file"""
        # Try environment variable first
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            return db_url
        
        # Try to read from .env file
        try:
            env_path = os.path.join(os.path.dirname(__file__), '../../backend-v2/.env')
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('DATABASE_URL='):
                        return line.split('=', 1)[1]
        except FileNotFoundError:
            pass
        
        return None
    
    def connect(self):
        """Create database connection"""
        try:
            return psycopg2.connect(self.database_url)
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            sys.exit(1)
    
    def execute_sql(self, sql: str, params: tuple = None):
        """Execute SQL statement"""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
                print(f"✅ Executed: {sql[:80]}{'...' if len(sql) > 80 else ''}")
        except Exception as e:
            print(f"❌ Failed to execute SQL: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    );
                """, (table_name,))
                return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def column_exists(self, table_name: str, column_name: str) -> bool:
        """Check if column exists in table"""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_name = %s AND column_name = %s
                    );
                """, (table_name, column_name))
                return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def create_user_learning_paths_table(self):
        """Create user_learning_paths table for enrollment tracking"""
        if self.table_exists('user_learning_paths'):
            print("✅ user_learning_paths table already exists")
            return
        
        sql = """
        CREATE TABLE user_learning_paths (
            id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            learning_path_id VARCHAR(255) NOT NULL,
            progress INTEGER DEFAULT 0,
            enrolled_at TIMESTAMP DEFAULT NOW(),
            completed_at TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(user_id, learning_path_id)
        );
        
        -- Add indexes for performance
        CREATE INDEX idx_user_learning_paths_user_id ON user_learning_paths(user_id);
        CREATE INDEX idx_user_learning_paths_learning_path_id ON user_learning_paths(learning_path_id);
        """
        
        self.execute_sql(sql)
        print("✅ Created user_learning_paths table with indexes")
    
    def add_missing_learning_paths_columns(self):
        """Add any missing columns to learning_paths table"""
        if not self.table_exists('learning_paths'):
            print("❌ learning_paths table does not exist")
            return
        
        # Add user_id column if it doesn't exist (for ownership)
        if not self.column_exists('learning_paths', 'user_id'):
            sql = "ALTER TABLE learning_paths ADD COLUMN user_id VARCHAR(255);"
            self.execute_sql(sql)
            print("✅ Added user_id column to learning_paths table")
        
        # Add status column if it doesn't exist
        if not self.column_exists('learning_paths', 'status'):
            sql = "ALTER TABLE learning_paths ADD COLUMN status VARCHAR(50) DEFAULT 'active';"
            self.execute_sql(sql)
            print("✅ Added status column to learning_paths table")
    
    def run_learning_path_updates(self):
        """Run all learning path related database updates"""
        print("🚀 Running learning path database updates...")
        self.create_user_learning_paths_table()
        self.add_missing_learning_paths_columns()
        print("✅ Learning path database updates completed!")

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python db_update_tool.py <command>")
        print("Commands:")
        print("  learning-paths  - Run learning path database updates")
        print("  create-table <table_name> - Create a specific table")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        updater = DatabaseUpdater()
        
        if command == "learning-paths":
            updater.run_learning_path_updates()
        elif command == "create-table" and len(sys.argv) > 2:
            table_name = sys.argv[2]
            if table_name == "user_learning_paths":
                updater.create_user_learning_paths_table()
            else:
                print(f"❌ Unknown table: {table_name}")
        else:
            print(f"❌ Unknown command: {command}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()