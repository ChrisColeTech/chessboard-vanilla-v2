import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { UserSessionResponse, CreateUserSessionRequest, UpdateUserSessionRequest } from '../models/UserSession';

export class UserSessionService {
  private db = Database.getInstance();

async updateUserSession(id: string, data: UpdateUserSessionRequest): Promise<UserSessionResponse> {
    const result = await this.db.query(`
      UPDATE user_sessions 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('UserSession not found');
    return this.formatUserSessionResponse(result.rows[0]);
  }

async getAllUser_sessions(): Promise<UserSessionResponse[]> {
    const result = await this.db.query('SELECT * FROM user_sessions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserSessionResponse(row));
  }

async getUserSessionById(id: string): Promise<UserSessionResponse> {
    const result = await this.db.query('SELECT * FROM user_sessions WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('UserSession not found');
    
    return this.formatUserSessionResponse(result.rows[0]);
  }

  async getUserSessionsByUserId(...args: any[]): Promise<any> {
    // Generic implementation for getUserSessionsByUserId
    const result = await this.db.query('SELECT * FROM user_sessions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserSessionResponse(row));
  }

  async cleanupExpiredSessions(...args: any[]): Promise<any> {
    // Generic implementation for cleanupExpiredSessions
    const result = await this.db.query('SELECT * FROM user_sessions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserSessionResponse(row));
  }

async listUserSessions(): Promise<UserSessionResponse[]> {
    const result = await this.db.query('SELECT * FROM user_sessions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserSessionResponse(row));
  }

async createUserSession(data: CreateUserSessionRequest): Promise<UserSessionResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO user_sessions (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatUserSessionResponse(result.rows[0]);
  }

async deleteUserSession(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM user_sessions WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('UserSession not found');
  }

private formatUserSessionResponse(row: any): UserSessionResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      refresh_token: row.refresh_token,
      expires_at: row.expires_at,
      ip_address: row.ip_address,
      user_agent: row.user_agent,
      created_at: row.created_at,
      last_accessed: row.last_accessed,
    };
  }
}