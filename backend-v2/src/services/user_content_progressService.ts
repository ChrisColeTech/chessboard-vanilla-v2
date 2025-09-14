import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { UserContentProgressResponse, CreateUserContentProgressRequest, UpdateUserContentProgressRequest } from '../models/UserContentProgress';

export class UserContentProgressService {
  private db = Database.getInstance();

async createUserContentProgress(data: CreateUserContentProgressRequest): Promise<UserContentProgressResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO user_content_progress (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatUserContentProgressResponse(result.rows[0]);
  }

async updateUserContentProgress(id: string, data: UpdateUserContentProgressRequest): Promise<UserContentProgressResponse> {
    const result = await this.db.query(`
      UPDATE user_content_progress 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('UserContentProgress not found');
    return this.formatUserContentProgressResponse(result.rows[0]);
  }

async deleteUserContentProgress(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM user_content_progress WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('UserContentProgress not found');
  }

  async getUserContentProgressByContent(...args: any[]): Promise<any> {
    // Generic implementation for getUserContentProgressByContent
    const result = await this.db.query('SELECT * FROM user_content_progress ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserContentProgressResponse(row));
  }

async listUserContentProgress(): Promise<UserContentProgressResponse[]> {
    const result = await this.db.query('SELECT * FROM user_content_progress ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserContentProgressResponse(row));
  }

async getAllUser_content_progress(): Promise<UserContentProgressResponse[]> {
    const result = await this.db.query('SELECT * FROM user_content_progress ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserContentProgressResponse(row));
  }

  async getUserContentProgressByUser(...args: any[]): Promise<any> {
    // Generic implementation for getUserContentProgressByUser
    const result = await this.db.query('SELECT * FROM user_content_progress ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserContentProgressResponse(row));
  }

async getUserContentProgressById(id: string): Promise<UserContentProgressResponse> {
    const result = await this.db.query('SELECT * FROM user_content_progress WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('UserContentProgress not found');
    
    return this.formatUserContentProgressResponse(result.rows[0]);
  }

private formatUserContentProgressResponse(row: any): UserContentProgressResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      content_id: row.content_id,
      status: row.status,
      progress_percentage: row.progress_percentage,
      time_spent: row.time_spent,
      completion_score: row.completion_score,
      started_at: row.started_at,
      completed_at: row.completed_at,
      last_accessed: row.last_accessed,
      notes: row.notes,
      bookmarked: row.bookmarked,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}