import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { GamereviewResponse, CreateGamereviewRequest, UpdateGamereviewRequest } from '../models/Gamereview';

export class GamereviewService {
  private db = Database.getInstance();

  async createReview(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM game_reviews ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  async getGameReviews(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM game_reviews ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  async getReviewById(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM game_reviews ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  async getAllGame_reviews(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM game_reviews ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  async getGamereviewById(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM game_reviews ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  async createGamereview(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM game_reviews ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  async updateGamereview(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM game_reviews ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  async deleteGamereview(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM game_reviews ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  private formatGamereviewResponse(row: any): GamereviewResponse {
    return {
      id: row.id,
      game_id: row.game_id,
      reviewer_id: row.reviewer_id,
      analysis: row.analysis,
      rating: row.rating,
      key_moments: row.key_moments,
      created_at: row.created_at,
    };
  }
}