import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { AnalyticsResponse, CreateAnalyticsRequest, UpdateAnalyticsRequest } from '../models/Analytics';

export class AnalyticsService {
  private db = Database.getInstance();

  async trackEvent(...args: any[]): Promise<any> {
    const result = await this.db.query('SELECT * FROM user_analytics ORDER BY created_at DESC LIMIT 100');
    return result.rows.map(row => this.formatAnalyticsResponse(row));
  }

  async getUserAnalytics(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM user_analytics ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAnalyticsResponse(row));
  }

  async getAnalyticsSummary(): Promise<AnalyticsResponse[]> {
    const result = await this.db.query('SELECT * FROM user_analytics ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAnalyticsResponse(row));
  }

  async getAllAnalytics(): Promise<AnalyticsResponse[]> {
    const result = await this.db.query('SELECT * FROM user_analytics ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAnalyticsResponse(row));
  }

  async getAnalyticsById(id: string): Promise<AnalyticsResponse> {
    const result = await this.db.query('SELECT * FROM user_analytics WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Analytics not found');
    
    return this.formatAnalyticsResponse(result.rows[0]);
  }

  async createAnalytics(data: CreateAnalyticsRequest): Promise<AnalyticsResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO user_analytics (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatAnalyticsResponse(result.rows[0]);
  }

  async updateAnalytics(id: string, data: UpdateAnalyticsRequest): Promise<AnalyticsResponse> {
    const result = await this.db.query(`
      UPDATE user_analytics 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Analytics not found');
    return this.formatAnalyticsResponse(result.rows[0]);
  }

  async deleteAnalytics(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM user_analytics WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Analytics not found');
  }

  private formatAnalyticsResponse(row: any): AnalyticsResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      event_type: row.event_type,
      event_data: row.event_data,
      timestamp: row.timestamp,
      session_id: row.session_id,
    };
  }
}