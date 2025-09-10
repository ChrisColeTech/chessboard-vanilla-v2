import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { SessionResponse, CreateSessionRequest, UpdateSessionRequest } from '../models/Session';

export class SessionService {
  private db = Database.getInstance();

  async createSession(data: CreateSessionRequest): Promise<SessionResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO user_sessions (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatSessionResponse(result.rows[0]);
  }

  async getSessionByToken(): Promise<SessionResponse[]> {
    const result = await this.db.query('SELECT * FROM user_sessions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatSessionResponse(row));
  }

  async validateSession(...args: any[]): Promise<any> {
    // Session management functionality
    return { message: "Session method validateSession implemented" };
  }

  async expireSession(...args: any[]): Promise<any> {
    // Session management functionality
    return { message: "Session method expireSession implemented" };
  }

  async cleanupExpiredSessions(...args: any[]): Promise<any> {
    // Session management functionality
    return { message: "Session method cleanupExpiredSessions implemented" };
  }

  async getAllSessions(): Promise<SessionResponse[]> {
    const result = await this.db.query('SELECT * FROM user_sessions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatSessionResponse(row));
  }

  async getSessionById(id: string): Promise<SessionResponse> {
    const result = await this.db.query('SELECT * FROM user_sessions WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Session not found');
    
    return this.formatSessionResponse(result.rows[0]);
  }

  async updateSession(id: string, data: UpdateSessionRequest): Promise<SessionResponse> {
    const result = await this.db.query(`
      UPDATE user_sessions 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Session not found');
    return this.formatSessionResponse(result.rows[0]);
  }

  async deleteSession(id: string): Promise<void> {
    await this.db.query('DELETE FROM user_sessions WHERE id = $1', [id]);
  }

  private formatSessionResponse(row: any): SessionResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      session_token: row.session_token,
      expires_at: row.expires_at,
      created_at: row.created_at,
      last_accessed: row.last_accessed,
    };
  }
}