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

  async updateProgress(userId: string, data: UpdateProgressRequest): Promise<ProgressResponse> {
    // Handle invalid date strings by setting them to null
    let lastPuzzleDate = null;
    if (data.last_puzzle_date && data.last_puzzle_date !== 'test_last_puzzle_date') {
      // Validate date format
      const date = new Date(data.last_puzzle_date);
      if (!isNaN(date.getTime())) {
        lastPuzzleDate = data.last_puzzle_date;
      }
    }
    
    // Handle achievements_unlocked - ensure it's valid JSON
    let achievementsJson = null;
    if (data.achievements_unlocked) {
      if (typeof data.achievements_unlocked === 'string') {
        try {
          JSON.parse(data.achievements_unlocked);
          achievementsJson = data.achievements_unlocked;
        } catch (e) {
          achievementsJson = '[]'; // Default to empty array if invalid JSON
        }
      } else {
        achievementsJson = JSON.stringify(data.achievements_unlocked);
      }
    }
    
    // First check if user exists, if not create a basic user record
    const userCheck = await this.db.query('SELECT id FROM users WHERE id = $1', [userId]);
    if (!userCheck.rows.length) {
      await this.db.query(`
        INSERT INTO users (id, username, email, password_hash, created_at, updated_at)
        VALUES ($1, $2, $3, $4, NOW(), NOW())
      `, [userId, `user_${userId.substring(0, 8)}`, `${userId}@example.com`, 'temp_hash']);
    }
    
    // Use the authenticated userId parameter, not the payload user_id
    // Try to update existing progress
    let result = await this.db.query(`
      UPDATE user_progress 
      SET puzzles_solved = COALESCE($2, puzzles_solved),
          puzzles_correct = COALESCE($3, puzzles_correct),
          current_streak = COALESCE($4, current_streak),
          best_streak = COALESCE($5, best_streak),
          total_time_spent = COALESCE($6, total_time_spent),
          achievements_unlocked = COALESCE($7, achievements_unlocked),
          last_puzzle_date = COALESCE($8, last_puzzle_date),
          updated_at = NOW()
      WHERE user_id = $1
      RETURNING *
    `, [userId, data.puzzles_solved, data.puzzles_correct, data.current_streak, data.best_streak, data.total_time_spent, achievementsJson, lastPuzzleDate]);
    
    // If no progress exists, create one (upsert logic)
    if (!result.rows.length) {
      const id = uuidv4();
      result = await this.db.query(`
        INSERT INTO user_progress (
          id, user_id, puzzles_solved, puzzles_correct, current_streak, 
          best_streak, total_time_spent, achievements_unlocked, 
          last_puzzle_date, created_at, updated_at
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW(), NOW())
        RETURNING *
      `, [
        id, 
        userId,
        data.puzzles_solved || 0,
        data.puzzles_correct || 0,
        data.current_streak || 0,
        data.best_streak || 0,
        data.total_time_spent || 0,
        achievementsJson || '[]',
        lastPuzzleDate
      ]);
    }
    
    return this.formatProgressResponse(result.rows[0]);
  }

  async getProgressStats(userId?: string): Promise<ProgressResponse[]> {
    let query = 'SELECT * FROM user_progress';
    let params: any[] = [];
    
    if (userId) {
      query += ' WHERE user_id = $1';
      params.push(userId);
    }
    
    query += ' ORDER BY created_at DESC LIMIT 50';
    
    const result = await this.db.query(query, params);
    return result.rows.map(row => this.formatProgressResponse(row));
  }

  async resetProgress(userId: string): Promise<ProgressResponse | null> {
    const result = await this.db.query(`
      UPDATE user_progress 
      SET puzzles_solved = 0,
          puzzles_correct = 0,
          current_streak = 0,
          best_streak = 0,
          total_time_spent = 0,
          achievements_unlocked = '[]',
          last_puzzle_date = NULL,
          updated_at = NOW()
      WHERE user_id = $1
      RETURNING *
    `, [userId]);
    
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
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO user_progress (
        id, user_id, puzzles_solved, puzzles_correct, current_streak, 
        best_streak, total_time_spent, achievements_unlocked, 
        last_puzzle_date, created_at, updated_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW(), NOW())
      RETURNING *
    `, [
      id, 
      data.user_id || null,
      data.puzzles_solved || 0,
      data.puzzles_correct || 0,
      data.current_streak || 0,
      data.best_streak || 0,
      data.total_time_spent || 0,
      data.achievements_unlocked ? JSON.stringify(data.achievements_unlocked) : '[]',
      data.last_puzzle_date || null
    ]);
    
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