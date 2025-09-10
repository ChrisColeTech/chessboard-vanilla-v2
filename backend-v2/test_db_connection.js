const { Pool } = require('pg');
require('dotenv').config();

console.log('🔍 Testing database connection...');
console.log('DATABASE_URL set:', !!process.env.DATABASE_URL);
console.log('DB_HOST:', process.env.DB_HOST || 'not set');

let pool;
if (process.env.DATABASE_URL) {
  console.log('Using DATABASE_URL');
  pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
  });
} else {
  console.log('Using individual env vars');
  pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    database: process.env.DB_NAME || 'chessboard',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'password',
    ssl: false
  });
}

async function testConnection() {
  try {
    console.log('🔗 Attempting to connect...');
    const client = await pool.connect();
    console.log('✅ Connected successfully!');
    
    const result = await client.query('SELECT NOW()');
    console.log('⏰ Server time:', result.rows[0].now);
    
    client.release();
    await pool.end();
    
    console.log('🎉 Database connection test passed!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Database connection failed:', error.message);
    process.exit(1);
  }
}

testConnection();