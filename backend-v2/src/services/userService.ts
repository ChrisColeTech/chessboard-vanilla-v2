import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { UserResponse, CreateUserRequest, UpdateUserRequest } from '../models/User';

export class UserService {
  private db = Database.getInstance();

  async getUserProfile(userId: string): Promise<UserResponse> {
    const result = await this.db.query('SELECT * FROM users WHERE id = $1', [userId]);
    if (!result.rows.length) throw new Error('User not found');
    
    return this.formatUserResponse(result.rows[0]);
  }

  async updateUserProfile(userId: string, profileData: any): Promise<UserResponse> {
    const result = await this.db.query(`
      UPDATE users 
      SET chess_elo = $1, puzzle_rating = $2, updated_at = NOW()
      WHERE id = $3
      RETURNING *
    `, [
      profileData.chess_elo,
      profileData.puzzle_rating,
      userId
    ]);
    
    if (!result.rows.length) throw new Error('User not found');
    return this.formatUserResponse(result.rows[0]);
  }

  async getUserPreferences(userId: string): Promise<UserResponse> {
    const result = await this.db.query('SELECT * FROM users WHERE id = $1', [userId]);
    if (!result.rows.length) throw new Error('User not found');
    
    return this.formatUserResponse(result.rows[0]);
  }

  async updateUserPreferences(userId: string, preferencesData: any): Promise<UserResponse> {
    const result = await this.db.query(`
      UPDATE users 
      SET preferences = $1, updated_at = NOW()
      WHERE id = $2
      RETURNING *
    `, [
      JSON.stringify(preferencesData),
      userId
    ]);
    
    if (!result.rows.length) throw new Error('User not found');
    return this.formatUserResponse(result.rows[0]);
  }

  async getUserSettings(userId: string): Promise<UserResponse> {
    const result = await this.db.query('SELECT * FROM users WHERE id = $1', [userId]);
    if (!result.rows.length) throw new Error('User not found');
    
    return this.formatUserResponse(result.rows[0]);
  }

  async updateUserSettings(userId: string, settingsData: any): Promise<UserResponse> {
    const result = await this.db.query(`
      UPDATE users 
      SET chess_elo = $1, puzzle_rating = $2, updated_at = NOW()
      WHERE id = $3
      RETURNING *
    `, [
      settingsData.chess_elo,
      settingsData.puzzle_rating,
      userId
    ]);
    
    if (!result.rows.length) throw new Error('User not found');
    return this.formatUserResponse(result.rows[0]);
  }

  async getAllUsers(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

  async getUserById(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

  async createUser(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

  async updateUser(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

  async deleteUser(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

  private formatUserResponse(row: any): UserResponse {
    return {
      id: row.id,
      username: row.username,
      email: row.email,
      password_hash: row.password_hash,
      chess_elo: row.chess_elo,
      puzzle_rating: row.puzzle_rating,
      preferences: row.preferences,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}