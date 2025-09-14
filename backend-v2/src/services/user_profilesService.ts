import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { UserProfileResponse, CreateUserProfileRequest, UpdateUserProfileRequest } from '../models/UserProfile';

export class UserProfileService {
  private db = Database.getInstance();

async listUserProfiles(): Promise<UserProfileResponse[]> {
    const result = await this.db.query('SELECT * FROM user_profiles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserProfileResponse(row));
  }

async updateUserProfile(id: string, data: UpdateUserProfileRequest): Promise<UserProfileResponse> {
    const result = await this.db.query(`
      UPDATE user_profiles 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('UserProfile not found');
    return this.formatUserProfileResponse(result.rows[0]);
  }

async getUserProfileById(id: string): Promise<UserProfileResponse> {
    const result = await this.db.query('SELECT * FROM user_profiles WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('UserProfile not found');
    
    return this.formatUserProfileResponse(result.rows[0]);
  }

async deleteUserProfile(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM user_profiles WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('UserProfile not found');
  }

async getAllUser_profiles(): Promise<UserProfileResponse[]> {
    const result = await this.db.query('SELECT * FROM user_profiles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserProfileResponse(row));
  }

async createUserProfile(data: CreateUserProfileRequest): Promise<UserProfileResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO user_profiles (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatUserProfileResponse(result.rows[0]);
  }

  async getUserProfileByUserId(...args: any[]): Promise<any> {
    // Generic implementation for getUserProfileByUserId
    const result = await this.db.query('SELECT * FROM user_profiles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserProfileResponse(row));
  }

private formatUserProfileResponse(row: any): UserProfileResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      display_name: row.display_name,
      avatar_url: row.avatar_url,
      bio: row.bio,
      country: row.country,
      timezone: row.timezone,
      board_preferences: row.board_preferences,
      profile_visibility: row.profile_visibility,
      show_rating: row.show_rating,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}