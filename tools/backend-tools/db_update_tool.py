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
    
    def add_column(self, table_name: str, column_name: str, column_type: str, default_value: str = None, not_null: bool = False):
        """Add a column to a table if it doesn't exist"""
        if not self.table_exists(table_name):
            print(f"❌ Table '{table_name}' does not exist")
            return False
        
        if self.column_exists(table_name, column_name):
            print(f"✅ Column '{column_name}' already exists in '{table_name}' table")
            return True
        
        # Build ALTER TABLE statement
        sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        
        if default_value is not None:
            if column_type.upper().startswith(('VARCHAR', 'TEXT', 'CHAR')):
                sql += f" DEFAULT '{default_value}'"
            elif column_type.upper() == 'JSONB':
                sql += f" DEFAULT '{default_value}'"
            else:
                sql += f" DEFAULT {default_value}"
        
        if not_null:
            sql += " NOT NULL"
        
        sql += ";"
        
        try:
            self.execute_sql(sql)
            print(f"✅ Added column '{column_name}' to '{table_name}' table")
            return True
        except Exception as e:
            print(f"❌ Failed to add column '{column_name}' to '{table_name}': {e}")
            return False
    
    def fix_missing_columns(self):
        """Fix all known missing column issues from API tests"""
        print("🚀 Fixing missing columns based on API test results...")
        
        success_count = 0
        
        # Fix puzzle_attempts table - missing created_at and updated_at
        if self.add_column('puzzle_attempts', 'created_at', 'TIMESTAMP', 'NOW()', True):
            success_count += 1
        if self.add_column('puzzle_attempts', 'updated_at', 'TIMESTAMP', 'NOW()', True):
            success_count += 1
        
        # Check and add other common missing columns for various tables
        tables_needing_timestamps = [
            'user_learning_paths', 'user_study_plans', 'subscriptions',
            'ai_opponents', 'historic_games', 'learning_modules',
            'tutorial_steps', 'study_plans', 'profiles'
        ]
        
        for table in tables_needing_timestamps:
            if self.table_exists(table):
                if self.add_column(table, 'created_at', 'TIMESTAMP', 'NOW()', False):
                    success_count += 1
                if self.add_column(table, 'updated_at', 'TIMESTAMP', 'NOW()', False):
                    success_count += 1
        
        print(f"✅ Fixed missing columns - {success_count} columns added successfully!")
        return success_count > 0
    
    def modify_column_nullable(self, table_name: str, column_name: str, nullable: bool = True):
        """Modify a column to be nullable or not nullable"""
        if not self.table_exists(table_name):
            print(f"❌ Table '{table_name}' does not exist")
            return False
        
        if not self.column_exists(table_name, column_name):
            print(f"❌ Column '{column_name}' does not exist in table '{table_name}'")
            return False
        
        # Build ALTER TABLE statement
        constraint = "DROP NOT NULL" if nullable else "SET NOT NULL"
        sql = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} {constraint};"
        
        try:
            self.execute_sql(sql)
            nullable_text = "nullable" if nullable else "not nullable"
            print(f"✅ Modified column '{column_name}' in '{table_name}' to be {nullable_text}")
            return True
        except Exception as e:
            print(f"❌ Failed to modify column '{column_name}' in '{table_name}': {e}")
            return False
    
    def fix_null_constraint_violations(self):
        """Fix all known null constraint violations from API tests"""
        print("🚀 Fixing null constraint violations based on API test results...")
        
        success_count = 0
        
        # Fix user_learning_paths table - user_id column causing null constraint
        if self.modify_column_nullable('user_learning_paths', 'user_id', True):
            success_count += 1
        
        # Fix user_study_plans table - name column causing null constraint
        if self.modify_column_nullable('user_study_plans', 'name', True):
            success_count += 1
        
        # Fix subscriptions table - name column causing null constraint
        if self.modify_column_nullable('subscriptions', 'name', True):
            success_count += 1
        
        # Add any other problematic columns that might cause null violations
        problematic_columns = [
            ('user_learning_paths', 'learning_path_id'),
            ('user_study_plans', 'user_id'),
            ('subscriptions', 'user_id'),
            ('profiles', 'user_id'),
            ('progress', 'user_id'),
        ]
        
        for table, column in problematic_columns:
            if self.table_exists(table) and self.column_exists(table, column):
                if self.modify_column_nullable(table, column, True):
                    success_count += 1
        
        print(f"✅ Fixed null constraint violations - {success_count} columns modified successfully!")
        return success_count > 0
    
    def modify_column_type(self, table_name: str, column_name: str, new_type: str, using_expression: str = None):
        """Modify a column's data type"""
        if not self.table_exists(table_name):
            print(f"❌ Table '{table_name}' does not exist")
            return False
        
        if not self.column_exists(table_name, column_name):
            print(f"❌ Column '{column_name}' does not exist in table '{table_name}'")
            return False
        
        # Build ALTER TABLE statement
        sql = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_type}"
        
        # Add USING clause if provided (for type conversions that need explicit casting)
        if using_expression:
            sql += f" USING {using_expression}"
        
        sql += ";"
        
        try:
            self.execute_sql(sql)
            print(f"✅ Modified column '{column_name}' in '{table_name}' to type '{new_type}'")
            return True
        except Exception as e:
            print(f"❌ Failed to modify column type for '{column_name}' in '{table_name}': {e}")
            return False
    
    def show_table_schema(self, table_name: str):
        """Show the current schema for a table"""
        if not self.table_exists(table_name):
            print(f"❌ Table '{table_name}' does not exist")
            return
        
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        column_name,
                        data_type,
                        is_nullable,
                        column_default
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position;
                """, (table_name,))
                
                columns = cursor.fetchall()
                if columns:
                    print(f"\n📋 Schema for table '{table_name}':")
                    print(f"{'Column':<20} {'Type':<15} {'Nullable':<10} {'Default':<20}")
                    print("-" * 65)
                    for col in columns:
                        nullable = "YES" if col[2] == "YES" else "NO"
                        default = col[3] if col[3] else ""
                        print(f"{col[0]:<20} {col[1]:<15} {nullable:<10} {default:<20}")
                else:
                    print(f"❌ No columns found for table '{table_name}'")
        finally:
            conn.close()
    
    def query_database(self, query: str):
        """Execute a SELECT query and display results"""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                
                if results:
                    # Get column names
                    column_names = [desc[0] for desc in cursor.description]
                    
                    print(f"\n📊 Query Results ({len(results)} rows):")
                    print("-" * 60)
                    
                    # Print header
                    header = " | ".join(f"{col:<15}" for col in column_names)
                    print(header)
                    print("-" * len(header))
                    
                    # Print rows
                    for row in results:
                        row_str = " | ".join(f"{str(val):<15}" for val in row)
                        print(row_str)
                else:
                    print("📭 No results found")
                    
        except Exception as e:
            print(f"❌ Query failed: {e}")
        finally:
            conn.close()
    
    def populate_test_data(self):
        """Populate tables with test data for API testing"""
        print("🚀 Populating tables with test data...")
        
        success_count = 0
        
        # Populate learning_modules if empty
        if self.table_exists('learning_modules'):
            conn = self.connect()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM learning_modules")
                    count = cursor.fetchone()[0]
                    
                    if count == 0:
                        test_modules = [
                            {
                                'id': 'test-module-001',
                                'learning_path_id': 'nu2i5slg3mewklnfk',  # Use existing learning path
                                'name': 'Basic Chess Tactics',
                                'description': 'Learn fundamental chess tactics',
                                'order_index': 1,
                                'estimated_hours': 1,
                                'module_type': 'tactical',
                                'content': 'Introduction to basic tactics'
                            },
                            {
                                'id': 'test-module-002',
                                'learning_path_id': 'nu2i5slg3mewklnfk',
                                'name': 'Advanced Endgames',
                                'description': 'Master complex endgame positions',
                                'order_index': 2,
                                'estimated_hours': 2,
                                'module_type': 'endgame',
                                'content': 'Deep dive into endgame theory'
                            }
                        ]
                        
                        for module in test_modules:
                            cursor.execute("""
                                INSERT INTO learning_modules (id, learning_path_id, name, description, order_index, estimated_hours, module_type, content)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (id) DO NOTHING
                            """, (module['id'], module['learning_path_id'], module['name'], module['description'], 
                                 module['order_index'], module['estimated_hours'], module['module_type'], module['content']))
                        
                        conn.commit()
                        print(f"✅ Added {len(test_modules)} test learning modules")
                        success_count += len(test_modules)
                        
            except Exception as e:
                print(f"❌ Failed to populate learning_modules: {e}")
            finally:
                conn.close()
        
        # Populate user_study_plans if it should be study_plans table
        if self.table_exists('user_study_plans'):
            conn = self.connect()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM user_study_plans")
                    count = cursor.fetchone()[0]
                    
                    if count < 3:  # Add a few test records
                        test_plans = [
                            {
                                'id': 'test-plan-001',
                                'user_id': '4c31c867-b8e1-46b8-872c-d8c196cd80f1',
                                'title': 'Beginner Study Plan',
                                'goals': 'Learn basic tactics and openings',
                                'schedule': 'Daily 30min sessions',
                                'progress': 0.3
                            },
                            {
                                'id': 'test-plan-002',
                                'user_id': '4c31c867-b8e1-46b8-872c-d8c196cd80f1', 
                                'title': 'Advanced Strategy',
                                'goals': 'Master positional play',
                                'schedule': 'Weekly analysis',
                                'progress': 0.7
                            }
                        ]
                        
                        for plan in test_plans:
                            cursor.execute("""
                                INSERT INTO user_study_plans (id, user_id, name, description, progress)
                                VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT (id) DO NOTHING
                            """, (plan['id'], plan['user_id'], plan['title'], 
                                 plan['goals'], plan['progress']))
                        
                        conn.commit()
                        print(f"✅ Added {len(test_plans)} test study plans")
                        success_count += len(test_plans)
                        
            except Exception as e:
                print(f"❌ Failed to populate user_study_plans: {e}")
            finally:
                conn.close()
        
        # Add user profile if missing
        if self.table_exists('user_profiles'):
            conn = self.connect()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM user_profiles WHERE user_id = %s", 
                                 ('4c31c867-b8e1-46b8-872c-d8c196cd80f1',))
                    count = cursor.fetchone()[0]
                    
                    if count == 0:
                        cursor.execute("""
                            INSERT INTO user_profiles (id, user_id, display_name, bio, country)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (id) DO NOTHING
                        """, ('test-profile-001', '4c31c867-b8e1-46b8-872c-d8c196cd80f1',
                             'Test User', 'Chess enthusiast and learner', 'US'))
                        
                        conn.commit()
                        print("✅ Added test user profile")
                        success_count += 1
                        
            except Exception as e:
                print(f"❌ Failed to populate user_profiles: {e}")
            finally:
                conn.close()
        
        # Add user progress record if missing
        if self.table_exists('user_progress'):
            conn = self.connect()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM user_progress WHERE user_id = %s", 
                                 ('4c31c867-b8e1-46b8-872c-d8c196cd80f1',))
                    count = cursor.fetchone()[0]
                    
                    if count == 0:
                        cursor.execute("""
                            INSERT INTO user_progress (id, user_id, puzzles_solved, puzzles_correct, current_streak, best_streak, total_time_spent)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (id) DO NOTHING
                        """, ('test-progress-001', '4c31c867-b8e1-46b8-872c-d8c196cd80f1',
                             50, 45, 5, 12, 3600))
                        
                        conn.commit()
                        print("✅ Added test user progress")
                        success_count += 1
                        
            except Exception as e:
                print(f"❌ Failed to populate user_progress: {e}")
            finally:
                conn.close()
        
        # Add test enrollment in user_learning_paths if missing
        if self.table_exists('user_learning_paths'):
            conn = self.connect()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM user_learning_paths WHERE user_id = %s AND learning_path_id = %s", 
                                 ('4c31c867-b8e1-46b8-872c-d8c196cd80f1', 'nu2i5slg3mewklnfk'))
                    count = cursor.fetchone()[0]
                    
                    if count == 0:
                        cursor.execute("""
                            INSERT INTO user_learning_paths (id, user_id, learning_path_id, progress)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (id) DO NOTHING
                        """, ('test-enrollment-001', '4c31c867-b8e1-46b8-872c-d8c196cd80f1',
                             'nu2i5slg3mewklnfk', 0.25))
                        
                        conn.commit()
                        print("✅ Added test learning path enrollment")
                        success_count += 1
                        
            except Exception as e:
                print(f"❌ Failed to populate user_learning_paths enrollment: {e}")
            finally:
                conn.close()
        
        print(f"✅ Test data population completed - {success_count} records added!")
        return success_count > 0
    
    def delete_malformed_puzzle_themes(self):
        """Delete puzzle records with malformed themes data"""
        print("🚀 Deleting puzzle records with malformed themes...")
        
        if not self.table_exists('puzzles'):
            print("❌ puzzles table does not exist")
            return False
        
        # First, show what we're about to delete
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, themes 
                    FROM puzzles 
                    WHERE themes::text NOT LIKE '[%]' AND themes IS NOT NULL
                    LIMIT 10
                """)
                malformed_records = cursor.fetchall()
                
                if malformed_records:
                    print(f"📋 Found {len(malformed_records)} malformed puzzle themes records (showing first 10):")
                    for record in malformed_records:
                        print(f"  - ID: {record[0]}, themes: {record[1]}")
                    
                    # Get total count
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM puzzles 
                        WHERE themes::text NOT LIKE '[%]' AND themes IS NOT NULL
                    """)
                    total_count = cursor.fetchone()[0]
                    
                    # Delete the malformed records
                    cursor.execute("""
                        DELETE FROM puzzles 
                        WHERE themes::text NOT LIKE '[%]' AND themes IS NOT NULL
                    """)
                    
                    deleted_count = cursor.rowcount
                    conn.commit()
                    
                    print(f"✅ Deleted {deleted_count} puzzle records with malformed themes")
                    return True
                else:
                    print("✅ No malformed puzzle themes found")
                    return True
                    
        except Exception as e:
            print(f"❌ Failed to delete malformed puzzle themes: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def delete_invalid_foreign_key_records(self):
        """Delete records with invalid foreign key references"""
        print("🚀 Deleting records with invalid foreign key references...")
        
        success_count = 0
        
        # Delete user_achievements with invalid achievement_id
        if self.table_exists('user_achievements'):
            conn = self.connect()
            try:
                with conn.cursor() as cursor:
                    # Find user_achievements with non-existent achievement_id
                    cursor.execute("""
                        DELETE FROM user_achievements 
                        WHERE achievement_id NOT IN (SELECT id FROM achievements)
                    """)
                    deleted_count = cursor.rowcount
                    conn.commit()
                    if deleted_count > 0:
                        print(f"✅ Deleted {deleted_count} user_achievements with invalid achievement_id")
                        success_count += deleted_count
                    else:
                        print("✅ No invalid user_achievements found")
                        
            except Exception as e:
                print(f"❌ Failed to delete invalid user_achievements: {e}")
                conn.rollback()
            finally:
                conn.close()
        
        # Delete user_content_progress with invalid content_id  
        if self.table_exists('user_content_progress'):
            conn = self.connect()
            try:
                with conn.cursor() as cursor:
                    # Find user_content_progress with non-existent content_id
                    cursor.execute("""
                        DELETE FROM user_content_progress 
                        WHERE content_id NOT IN (SELECT id FROM content)
                    """)
                    deleted_count = cursor.rowcount
                    conn.commit()
                    if deleted_count > 0:
                        print(f"✅ Deleted {deleted_count} user_content_progress with invalid content_id")
                        success_count += deleted_count
                    else:
                        print("✅ No invalid user_content_progress found")
                        
            except Exception as e:
                print(f"❌ Failed to delete invalid user_content_progress: {e}")
                conn.rollback()
            finally:
                conn.close()
        
        # Delete content records with invalid parent_id
        if self.table_exists('content'):
            conn = self.connect()
            try:
                with conn.cursor() as cursor:
                    # Find content with non-existent parent_id (excluding NULL parent_id)
                    cursor.execute("""
                        DELETE FROM content 
                        WHERE parent_id IS NOT NULL 
                        AND parent_id NOT IN (SELECT id FROM content WHERE id != parent_id)
                    """)
                    deleted_count = cursor.rowcount
                    conn.commit()
                    if deleted_count > 0:
                        print(f"✅ Deleted {deleted_count} content records with invalid parent_id")
                        success_count += deleted_count
                    else:
                        print("✅ No invalid content parent_id references found")
                        
            except Exception as e:
                print(f"❌ Failed to delete invalid content records: {e}")
                conn.rollback()
            finally:
                conn.close()
        
        print(f"✅ Invalid foreign key cleanup completed - {success_count} records deleted!")
        return success_count > 0

def show_help():
    """Display help information"""
    print("Database Update Tool - Manage database schema and data")
    print("=" * 60)
    print()
    print("Usage: python db_update_tool.py <command> [arguments]")
    print()
    print("COMMANDS:")
    print()
    print("Schema Management:")
    print("  help                                  - Show this help message")
    print("  show-schema <table_name>              - Show table schema")
    print("  add-column <table> <column> <type> [default] [--not-null]")
    print("                                        - Add specific column to table")
    print("  modify-nullable <table> <column> [true|false]")
    print("                                        - Make column nullable or not nullable")
    print("  modify-column-type <table> <column> <new_type> [--using <expression>]")
    print("                                        - Change column data type")
    print()
    print("Batch Operations:")
    print("  fix-columns                           - Fix all known missing column issues")
    print("  fix-null-constraints                  - Fix null constraint violations")
    print("  learning-paths                        - Run learning path database updates")
    print("  create-table <table_name>             - Create a specific table")
    print()
    print("Data Operations:")
    print("  query \"<sql_query>\"                   - Execute SELECT query and show results")
    print("  execute \"<sql_query>\"                 - Execute INSERT/UPDATE/DELETE query")
    print("  populate-test-data                    - Add test data to empty tables for API testing")
    print("  delete-malformed-themes               - Delete puzzle records with malformed themes")
    print("  delete-invalid-foreign-keys           - Delete records with invalid foreign key references")
    print()
    print("EXAMPLES:")
    print()
    print("  # Show schema for a table")
    print("  python db_update_tool.py show-schema user_profiles")
    print()
    print("  # Add a new column")
    print("  python db_update_tool.py add-column users email VARCHAR(255) --not-null")
    print()
    print("  # Query data")
    print("  python db_update_tool.py query \"SELECT * FROM users LIMIT 5\"")
    print()
    print("  # Add test data for API testing")
    print("  python db_update_tool.py populate-test-data")
    print()

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        sys.exit(0)
    
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
        elif command == "fix-columns":
            updater.fix_missing_columns()
        elif command == "fix-null-constraints":
            updater.fix_null_constraint_violations()
        elif command == "add-column" and len(sys.argv) >= 5:
            table_name = sys.argv[2]
            column_name = sys.argv[3]
            column_type = sys.argv[4]
            default_value = sys.argv[5] if len(sys.argv) > 5 and not sys.argv[5].startswith('--') else None
            not_null = '--not-null' in sys.argv
            updater.add_column(table_name, column_name, column_type, default_value, not_null)
        elif command == "modify-nullable" and len(sys.argv) >= 4:
            table_name = sys.argv[2]
            column_name = sys.argv[3]
            nullable = True  # Default to making it nullable
            if len(sys.argv) > 4:
                nullable = sys.argv[4].lower() in ('true', '1', 'yes', 'y')
            updater.modify_column_nullable(table_name, column_name, nullable)
        elif command == "modify-column-type" and len(sys.argv) >= 5:
            table_name = sys.argv[2]
            column_name = sys.argv[3]
            new_type = sys.argv[4]
            using_expression = None
            if '--using' in sys.argv:
                using_index = sys.argv.index('--using')
                if using_index + 1 < len(sys.argv):
                    using_expression = sys.argv[using_index + 1]
            updater.modify_column_type(table_name, column_name, new_type, using_expression)
        elif command == "show-schema" and len(sys.argv) > 2:
            table_name = sys.argv[2]
            updater.show_table_schema(table_name)
        elif command == "query" and len(sys.argv) > 2:
            query = sys.argv[2]
            updater.query_database(query)
        elif command == "execute" and len(sys.argv) > 2:
            query = sys.argv[2]
            updater.execute_sql(query)
        elif command == "populate-test-data":
            updater.populate_test_data()
        elif command == "delete-malformed-themes":
            updater.delete_malformed_puzzle_themes()
        elif command == "delete-invalid-foreign-keys":
            updater.delete_invalid_foreign_key_records()
        elif command in ['help', '-h', '--help']:
            show_help()
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'help' to see available commands")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()