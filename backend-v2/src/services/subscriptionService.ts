import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { SubscriptionResponse, CreateSubscriptionRequest, UpdateSubscriptionRequest } from '../models/Subscription';

export class SubscriptionService {
  private db = Database.getInstance();

  async getUserSubscription(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM subscriptions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatSubscriptionResponse(row));
  }

  async createSubscription(data: CreateSubscriptionRequest): Promise<SubscriptionResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO subscriptions (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatSubscriptionResponse(result.rows[0]);
  }

  async updateSubscription(id: string, data: UpdateSubscriptionRequest): Promise<SubscriptionResponse> {
    const result = await this.db.query(`
      UPDATE subscriptions 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Subscription not found');
    return this.formatSubscriptionResponse(result.rows[0]);
  }

  async cancelSubscription(...args: any[]): Promise<any> {
    const result = await this.db.query('SELECT * FROM subscriptions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatSubscriptionResponse(row));
  }

  async getAllSubscriptions(): Promise<SubscriptionResponse[]> {
    const result = await this.db.query('SELECT * FROM subscriptions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatSubscriptionResponse(row));
  }

  async getSubscriptionById(id: string): Promise<SubscriptionResponse> {
    const result = await this.db.query('SELECT * FROM subscriptions WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Subscription not found');
    
    return this.formatSubscriptionResponse(result.rows[0]);
  }

  async deleteSubscription(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM subscriptions WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Subscription not found');
  }

  private formatSubscriptionResponse(row: any): SubscriptionResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      plan_type: row.plan_type,
      status: row.status,
      expires_at: row.expires_at,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}