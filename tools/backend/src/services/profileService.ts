import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { ProfileResponse, CreateProfileRequest, UpdateProfileRequest } from '../models/Profile';

export class ProfileService {
  private db = Database.getInstance();

  async getProfile(): Promise<ProfileResponse[]> {
    const result = await this.db.query('SELECT * FROM user_profiles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatProfileResponse(row));
  }

  async updateProfile(id: string, data: UpdateProfileRequest): Promise<ProfileResponse> {
    const result = await this.db.query(`
      UPDATE user_profiles 
      SET updated_at = NOW(), ...data
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Profile not found');
    return this.formatProfileResponse(result.rows[0]);
  }

  async getAllProfiles(): Promise<ProfileResponse[]> {
    const result = await this.db.query('SELECT * FROM user_profiles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatProfileResponse(row));
  }

  async getProfileById(id: string): Promise<ProfileResponse> {
    const result = await this.db.query('SELECT * FROM user_profiles WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Profile not found');
    
    return this.formatProfileResponse(result.rows[0]);
  }

  async createProfile(data: CreateProfileRequest): Promise<ProfileResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO user_profiles (id, created_at, updated_at, ...data)
      VALUES ($1, NOW(), NOW(), ...)
      RETURNING *
    `, [id]);
    
    return this.formatProfileResponse(result.rows[0]);
  }

  async deleteProfile(id: string): Promise<void> {
    await this.db.query('DELETE FROM user_profiles WHERE id = $1', [id]);
  }

  private formatProfileResponse(row: any): ProfileResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      display_name: row.display_name,
      avatar_url: row.avatar_url,
      bio: row.bio,
      country: row.country,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}