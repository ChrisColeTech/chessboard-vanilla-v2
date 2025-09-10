import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { GamereviewResponse, CreateGamereviewRequest, UpdateGamereviewRequest } from '../models/Gamereview';

export class GamereviewService {
  private db = Database.getInstance();

  async createReview(...args: any[]): Promise<any> {
    // TODO: Implement createReview
    throw new Error('createReview not implemented');
  }

  async getGameReviews(): Promise<GamereviewResponse[]> {
    const result = await this.db.query('SELECT * FROM game_reviews WHERE status = $1 ORDER BY created_at DESC LIMIT 20', ['completed']);
    return result.rows.map(row => this.formatGamereviewResponse(row));
  }

  async getReviewById(...args: any[]): Promise<any> {
    // TODO: Implement getReviewById
    throw new Error('getReviewById not implemented');
  }

  async getAllGame_reviews(...args: any[]): Promise<any> {
    // TODO: Implement getAllGame_reviews
    throw new Error('getAllGame_reviews not implemented');
  }

  async getGamereviewById(...args: any[]): Promise<any> {
    // TODO: Implement getGamereviewById
    throw new Error('getGamereviewById not implemented');
  }

  async createGamereview(...args: any[]): Promise<any> {
    // TODO: Implement createGamereview
    throw new Error('createGamereview not implemented');
  }

  async updateGamereview(...args: any[]): Promise<any> {
    // TODO: Implement updateGamereview
    throw new Error('updateGamereview not implemented');
  }

  async deleteGamereview(...args: any[]): Promise<any> {
    // TODO: Implement deleteGamereview
    throw new Error('deleteGamereview not implemented');
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