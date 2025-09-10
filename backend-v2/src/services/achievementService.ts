import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { AchievementResponse, CreateAchievementRequest, UpdateAchievementRequest } from '../models/Achievement';

export class AchievementService {
  private db = Database.getInstance();

  async getAllAchievements(): Promise<AchievementResponse[]> {
    const result = await this.db.query('SELECT * FROM achievements ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAchievementResponse(row));
  }

  async getAchievementById(id: string): Promise<AchievementResponse> {
    const result = await this.db.query('SELECT * FROM achievements WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Achievement not found');
    
    return this.formatAchievementResponse(result.rows[0]);
  }

  async getUserAchievements(...args: any[]): Promise<any> {
    // TODO: Implement getUserAchievements
    throw new Error('getUserAchievements not implemented');
  }

  async unlockAchievement(...args: any[]): Promise<any> {
    const result = await this.db.query('SELECT * FROM achievements ORDER BY created_at DESC');
    return result.rows.map(row => this.formatAchievementResponse(row));
  }

  async checkAchievements(...args: any[]): Promise<any> {
    const result = await this.db.query('SELECT * FROM achievements ORDER BY created_at DESC');
    return result.rows.map(row => this.formatAchievementResponse(row));
  }

  async createAchievement(data: CreateAchievementRequest): Promise<AchievementResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO achievements (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatAchievementResponse(result.rows[0]);
  }

  async updateAchievement(id: string, data: UpdateAchievementRequest): Promise<AchievementResponse> {
    const result = await this.db.query(`
      UPDATE achievements 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Achievement not found');
    return this.formatAchievementResponse(result.rows[0]);
  }

  async deleteAchievement(id: string): Promise<void> {
    await this.db.query('DELETE FROM achievements WHERE id = $1', [id]);
  }

  private formatAchievementResponse(row: any): AchievementResponse {
    return {
      id: row.id,
      title: row.title,
      description: row.description,
      icon: row.icon,
      points: row.points,
      criteria: row.criteria,
      created_at: row.created_at,
    };
  }
}