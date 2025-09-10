import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { ProgressResponse, CreateProgressRequest, UpdateProgressRequest } from '../models/Progress';

export class ProgressService {
  private db = Database.getInstance();

  async getUserProgress(...args: any[]): Promise<any> {
    // TODO: Implement getUserProgress
    throw new Error('getUserProgress not implemented');
  }

  async updateProgress(id: string, data: UpdateProgressRequest): Promise<ProgressResponse> {
    const result = await this.db.query(`
      UPDATE user_progress 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Progress not found');
    return this.formatProgressResponse(result.rows[0]);
  }

  async getProgressStats(): Promise<ProgressResponse[]> {
    const result = await this.db.query('SELECT * FROM user_progress ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatProgressResponse(row));
  }

  async resetProgress(...args: any[]): Promise<any> {
    const result = await this.db.query('SELECT * FROM user_progress ORDER BY created_at DESC');
    return result.rows.map(row => this.formatProgressResponse(row));
  }

  async getAllProgress(): Promise<ProgressResponse[]> {
    const result = await this.db.query('SELECT * FROM user_progress ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatProgressResponse(row));
  }

  async getProgressById(id: string): Promise<ProgressResponse> {
    const result = await this.db.query('SELECT * FROM user_progress WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Progress not found');
    
    return this.formatProgressResponse(result.rows[0]);
  }

  async createProgress(data: CreateProgressRequest): Promise<ProgressResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO user_progress (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatProgressResponse(result.rows[0]);
  }

  async deleteProgress(id: string): Promise<void> {
    await this.db.query('DELETE FROM user_progress WHERE id = $1', [id]);
  }

  private formatProgressResponse(row: any): ProgressResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      puzzles_solved: row.puzzles_solved,
      puzzles_correct: row.puzzles_correct,
      current_streak: row.current_streak,
      best_streak: row.best_streak,
      total_time_spent: row.total_time_spent,
      achievements_unlocked: row.achievements_unlocked,
      last_puzzle_date: row.last_puzzle_date,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}