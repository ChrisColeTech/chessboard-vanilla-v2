import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { ProgressResponse, CreateProgressRequest, UpdateProgressRequest } from '../models/Progress';

export class ProgressService {
  private db = Database.getInstance();

  async getUserProgress(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM user_progress ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatProgressResponse(row));
  }

  async updateProgress(pathId: string, userId: string, progressData: any): Promise<any> {
    // Update user's progress in the learning path
    const result = await this.db.query(`
      UPDATE user_learning_paths 
      SET progress = $3, updated_at = NOW()
      WHERE user_id = $1 AND learning_path_id = $2
      RETURNING *
    `, [userId, pathId, progressData.progress || 0]);
    
    if (!result.rows.length) throw new Error('Enrollment not found - user must enroll first');
    
    // Get the learning path details
    const pathResult = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [pathId]);
    if (!pathResult.rows.length) throw new Error('Learning path not found');
    
    const learningPath = this.formatLearningPathResponse(pathResult.rows[0]);
    return {
      ...learningPath,
      progress: result.rows[0].progress,
      updated_at: result.rows[0].updated_at
    };
  }

  async getProgressStats(): Promise<ProgressResponse[]> {
    const result = await this.db.query('SELECT * FROM user_progress ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatProgressResponse(row));
  }

  async resetProgress(userId: string): Promise<any> {
    const result = await this.db.query('SELECT * FROM user_progress WHERE user_id = $1', [userId]);
    return result.rows.length ? this.formatProgressResponse(result.rows[0]) : null;
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

  private formatLearningPathResponse(row: any): any {
    return {
      id: row.id,
      title: row.title,
      description: row.description,
      difficulty: row.difficulty,
      modules: row.modules,
      progress: row.progress,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}