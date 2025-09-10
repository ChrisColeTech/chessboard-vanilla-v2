import { Pool } from 'pg';

export class Database {
  private static instance: Database;
  private pool: Pool;

  private constructor() {
    this.pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
      max: 5,                           // Lower max for Supabase pooler compatibility
      min: 1,                           // Lower min to prevent connection exhaustion
      idleTimeoutMillis: 10000,         // Shorter idle timeout for Supabase
      connectionTimeoutMillis: 10000,   // Longer connection timeout
      allowExitOnIdle: false,           // Keep pool alive to prevent reconnection issues
      keepAlive: true,                  // Enable TCP keepalive
      keepAliveInitialDelayMillis: 10000 // TCP keepalive initial delay
    });

    // Handle pool errors with reconnection logic
    this.pool.on('error', (err) => {
      console.error('❌ Database pool error:', err);
      if (err.message && err.message.includes('termination')) {
        console.log('🔄 Database connection terminated, pool will handle reconnection');
      }
    });

    // Handle pool connect events
    this.pool.on('connect', (client) => {
      console.log('🔗 Database client connected');
      // Set statement timeout to prevent long-running queries
      client.query('SET statement_timeout = 30000');
    });

    // Handle pool disconnect events  
    this.pool.on('remove', (client) => {
      console.log('🔌 Database client disconnected');
    });
  }

  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  async query(text: string, params?: any[]) {
    let client;
    try {
      client = await this.pool.connect();
      const result = await client.query(text, params);
      return result;
    } catch (error) {
      console.error('❌ Database query error:', error);
      if (error.message && error.message.includes('termination')) {
        console.log('🔄 Query failed due to connection termination, retrying...');
        // Retry once on termination
        try {
          const newClient = await this.pool.connect();
          const result = await newClient.query(text, params);
          newClient.release();
          return result;
        } catch (retryError) {
          console.error('❌ Retry also failed:', retryError);
          throw retryError;
        }
      }
      throw error;
    } finally {
      if (client) {
        client.release();
      }
    }
  }

  async getPoolInfo() {
    return {
      totalCount: this.pool.totalCount,
      idleCount: this.pool.idleCount,
      waitingCount: this.pool.waitingCount
    };
  }

  async close() {
    await this.pool.end();
  }
}

export const db = Database.getInstance();
export default Database;