import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { UserResponse, CreateUserRequest, UpdateUserRequest } from '../models/User';

export class UserService {
  private db = Database.getInstance();

async createUser(data: CreateUserRequest): Promise<UserResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO users (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatUserResponse(result.rows[0]);
  }

  async getUserByUsername(...args: any[]): Promise<any> {
    // Generic implementation for getUserByUsername
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

  async getUserByEmail(...args: any[]): Promise<any> {
    // Generic implementation for getUserByEmail
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

async updateUser(id: string, data: UpdateUserRequest): Promise<UserResponse> {
    const result = await this.db.query(`
      UPDATE users 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('User not found');
    return this.formatUserResponse(result.rows[0]);
  }

async getUserById(id: string): Promise<UserResponse> {
    const result = await this.db.query('SELECT * FROM users WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('User not found');
    
    return this.formatUserResponse(result.rows[0]);
  }

async deleteUser(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM users WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('User not found');
  }

async updateUserStats(id: string, data: UpdateUserRequest): Promise<UserResponse> {
    const result = await this.db.query(`
      UPDATE users 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('User not found');
    return this.formatUserResponse(result.rows[0]);
  }

async listUsers(): Promise<UserResponse[]> {
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

async getAllUsers(): Promise<UserResponse[]> {
    const result = await this.db.query('SELECT * FROM users ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatUserResponse(row));
  }

private formatUserResponse(row: any): UserResponse {
    return {
      id: row.id,
      username: row.username,
      email: row.email,
      password_hash: row.password_hash,
      email_verified: row.email_verified,
      chess_elo: row.chess_elo,
      puzzle_rating: row.puzzle_rating,
      games_played: row.games_played,
      games_won: row.games_won,
      games_lost: row.games_lost,
      games_drawn: row.games_drawn,
      created_at: row.created_at,
      updated_at: row.updated_at,
      last_login: row.last_login,
    };
  }
}