import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { UserAchievementResponse, CreateUserAchievementRequest, UpdateUserAchievementRequest } from '../models/UserAchievement';

export class UserAchievementService {
  private db = Database.getInstance();

async createUserAchievement(data: CreateUserAchievementRequest): Promise<UserAchievementResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO user_achievements (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatUserAchievementResponse(result.rows[0]);
  }

  async getUserAchievementsByAchievement(...args: any[]): Promise<any> {
    // Generic implementation for getUserAchievementsByAchievement
    const result = await this.db.query('SELECT * FROM user_achievements ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserAchievementResponse(row));
  }

async getAllUser_achievements(): Promise<UserAchievementResponse[]> {
    const result = await this.db.query('SELECT * FROM user_achievements ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserAchievementResponse(row));
  }

  async getUserAchievementsByUser(...args: any[]): Promise<any> {
    // Generic implementation for getUserAchievementsByUser
    const result = await this.db.query('SELECT * FROM user_achievements ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserAchievementResponse(row));
  }

async deleteUserAchievement(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM user_achievements WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('UserAchievement not found');
  }

async updateUserAchievement(id: string, data: UpdateUserAchievementRequest): Promise<UserAchievementResponse> {
    const result = await this.db.query(`
      UPDATE user_achievements 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('UserAchievement not found');
    return this.formatUserAchievementResponse(result.rows[0]);
  }

async getUserAchievementById(id: string): Promise<UserAchievementResponse> {
    const result = await this.db.query('SELECT * FROM user_achievements WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('UserAchievement not found');
    
    return this.formatUserAchievementResponse(result.rows[0]);
  }

async listUserAchievements(): Promise<UserAchievementResponse[]> {
    const result = await this.db.query('SELECT * FROM user_achievements ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserAchievementResponse(row));
  }

private formatUserAchievementResponse(row: any): UserAchievementResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      achievement_id: row.achievement_id,
      current_progress: row.current_progress,
      target_progress: row.target_progress,
      progress_percentage: row.progress_percentage,
      is_completed: row.is_completed,
      is_notified: row.is_notified,
      started_at: row.started_at,
      completed_at: row.completed_at,
    };
  }
}