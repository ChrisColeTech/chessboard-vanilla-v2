import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { StatsResponse, CreateStatsRequest, UpdateStatsRequest } from '../models/Stats';

export class StatsService {
  private db = Database.getInstance();

  async getOverviewStats(): Promise<StatsResponse[]> {
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStatsResponse(row));
  }

  async getPuzzleStats(): Promise<StatsResponse[]> {
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStatsResponse(row));
  }

  async getGameStats(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStatsResponse(row));
  }

  async getProgressStats(): Promise<StatsResponse[]> {
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStatsResponse(row));
  }

  async getPerformanceStats(): Promise<StatsResponse[]> {
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStatsResponse(row));
  }

  async getRatingStats(): Promise<StatsResponse[]> {
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStatsResponse(row));
  }

  async getAllStats(): Promise<StatsResponse[]> {
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStatsResponse(row));
  }

  async getStatsById(id: string): Promise<StatsResponse> {
    const result = await this.db.query('SELECT * FROM users WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Stats not found');
    
    return this.formatStatsResponse(result.rows[0]);
  }

  async createStats(data: CreateStatsRequest): Promise<StatsResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO users (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatStatsResponse(result.rows[0]);
  }

  async updateStats(id: string, data: UpdateStatsRequest): Promise<StatsResponse> {
    const result = await this.db.query(`
      UPDATE users 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Stats not found');
    return this.formatStatsResponse(result.rows[0]);
  }

  async deleteStats(id: string): Promise<void> {
    await this.db.query('DELETE FROM users WHERE id = $1', [id]);
  }

  private formatStatsResponse(row: any): StatsResponse {
    return {
      user_id: row.user_id,
      total_puzzles: row.total_puzzles,
      correct_puzzles: row.correct_puzzles,
      puzzle_accuracy: row.puzzle_accuracy,
      avg_solve_time: row.avg_solve_time,
      current_rating: row.current_rating,
      games_played: row.games_played,
      games_won: row.games_won,
      win_rate: row.win_rate,
    };
  }
}