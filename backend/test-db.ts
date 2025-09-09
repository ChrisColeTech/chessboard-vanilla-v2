import { Database } from './src/utils/database';
import dotenv from 'dotenv';

dotenv.config();

async function testDatabase() {
  console.log('🔍 Testing PostgreSQL connection...');
  console.log('DATABASE_URL:', process.env.DATABASE_URL?.replace(/:([^@]+)@/, ':***@'));
  
  try {
    const db = Database.getInstance();
    await db.connect();
    console.log('✅ Connection successful!');
    
    // Test basic query
    console.log('\n🔍 Testing basic query...');
    const result = await db.query('SELECT version() as version, now() as current_time');
    console.log('✅ Query result:', {
      version: result.rows[0].version.substring(0, 50) + '...',
      current_time: result.rows[0].current_time
    });
    
    // Test tables exist
    console.log('\n🔍 Checking existing tables...');
    const tables = await db.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public'
      ORDER BY table_name
    `);
    
    console.log(`✅ Found ${tables.rows.length} tables:`);
    tables.rows.forEach((row: any) => {
      console.log(`  - ${row.table_name}`);
    });
    
    await db.close();
    console.log('\n✅ Database test completed successfully!');
    
  } catch (error) {
    console.error('❌ Database test failed:', error);
    process.exit(1);
  }
}

testDatabase();