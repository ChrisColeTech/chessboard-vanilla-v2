import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * GameReviews Domain API Client
 * Handles all game-reviews-related API operations
 */
export class GameReviewsAPIClient extends BaseAPIClient {
  async createReview(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/gameReviews/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getGameReviews(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/gameReviews/game/:gameId${queryString}`);
  }
  async getReviewById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/gameReviews/${id}`);
  }
}

export default GameReviewsAPIClient;
