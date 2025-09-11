import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { ProfileResponse, CreateProfileRequest, UpdateProfileRequest } from '../models/Profile';

export class ProfileService {
  private db = Database.getInstance();

  async getProfile(userId?: string): Promise<ProfileResponse[]> {
    let query = 'SELECT * FROM user_profiles';
    let params: any[] = [];
    
    if (userId) {
      query += ' WHERE user_id = $1';
      params.push(userId);
    }
    
    query += ' ORDER BY created_at DESC LIMIT 50';
    
    const result = await this.db.query(query, params);
    return result.rows.map(row => this.formatProfileResponse(row));
  }

  async updateProfile(userId: string, data: UpdateProfileRequest): Promise<ProfileResponse> {
    // First check if user exists, if not create a basic user record
    const userCheck = await this.db.query('SELECT id FROM users WHERE id = $1', [userId]);
    if (!userCheck.rows.length) {
      await this.db.query(`
        INSERT INTO users (id, username, email, password_hash, created_at, updated_at)
        VALUES ($1, $2, $3, $4, NOW(), NOW())
      `, [userId, `user_${userId.substring(0, 8)}`, `${userId}@example.com`, 'temp_hash']);
    }
    
    // First try to update existing profile
    let result = await this.db.query(`
      UPDATE user_profiles 
      SET display_name = COALESCE($2, display_name),
          avatar_url = COALESCE($3, avatar_url),
          bio = COALESCE($4, bio),
          country = COALESCE($5, country),
          timezone = COALESCE($6, timezone),
          updated_at = NOW()
      WHERE user_id = $1
      RETURNING *
    `, [userId, data.display_name, data.avatar_url, data.bio, data.country, data.timezone]);
    
    // If no profile exists, create one (upsert logic)
    if (!result.rows.length) {
      const profileId = uuidv4();
      result = await this.db.query(`
        INSERT INTO user_profiles (id, user_id, display_name, avatar_url, bio, country, timezone, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
        RETURNING *
      `, [profileId, userId, data.display_name, data.avatar_url, data.bio, data.country, data.timezone]);
    }
    
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
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO user_profiles (
        id, user_id, display_name, avatar_url, bio, country, timezone, created_at, updated_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
      RETURNING *
    `, [
      id, 
      data.user_id || null,
      data.display_name || null,
      data.avatar_url || null,
      data.bio || null,
      data.country || null,
      data.timezone || null
    ]);
    
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
      timezone: row.timezone,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}