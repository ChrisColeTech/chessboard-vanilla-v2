import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { AuthResponse, CreateAuthRequest, UpdateAuthRequest } from '../models/Auth';

export class AuthService {
  private db = Database.getInstance();

  async register(registerData: any): Promise<any> {
    const { username, email, password } = registerData;

    // Check if user already exists
    const existingUser = await this.db.query(
      'SELECT id FROM users WHERE email = $1 OR username = $2',
      [email, username]
    );

    if (existingUser.rows.length > 0) {
      throw new Error('User with this email or username already exists');
    }

    // Hash password
    const bcrypt = require('bcrypt');
    const passwordHash = await bcrypt.hash(password, 12);

    // Create user
    const userId = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO users (id, username, email, password_hash, chess_elo, puzzle_rating, preferences, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
      RETURNING *
    `, [userId, username, email, passwordHash, 1000, 1000, '{}']);

    if (!result.rows.length) {
      throw new Error('Failed to create user');
    }

    return this.formatUserInfo(result.rows[0]);
  }

  async login(loginData: any): Promise<any> {
    const { email, password } = loginData;

    // Find user by email
    const result = await this.db.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );

    if (!result.rows.length) {
      throw new Error('Invalid credentials');
    }

    const user = result.rows[0];

    // Verify password
    const bcrypt = require('bcrypt');
    const isValidPassword = await bcrypt.compare(password, user.password_hash);
    if (!isValidPassword) {
      throw new Error('Invalid credentials');
    }

    // Generate JWT token
    const jwt = require('jsonwebtoken');
    const token = jwt.sign(
      { 
        userId: user.id, 
        email: user.email,
        username: user.username 
      },
      process.env.JWT_SECRET!,
      { expiresIn: '7d' }
    );

    return {
      user: this.formatUserInfo(user),
      token
    };
  }

  async getCurrentUser(userId: string): Promise<any> {
    // Get user info
    const userResult = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [userId]
    );

    if (!userResult.rows.length) {
      throw new Error('User not found');
    }

    // Get user progress (or create default if doesn't exist)
    let progressResult = await this.db.query(
      'SELECT * FROM user_progress WHERE user_id = $1',
      [userId]
    );

    // If no progress exists, create default progress
    if (!progressResult.rows.length) {
      const progressId = require('uuid').v4();
      await this.db.query(`
        INSERT INTO user_progress 
        (id, user_id, puzzles_solved, puzzles_correct, current_streak, best_streak, 
         total_time_spent, achievements_unlocked, created_at, updated_at)
        VALUES ($1, $2, 0, 0, 0, 0, 0, '[]', NOW(), NOW())
      `, [progressId, userId]);
      
      progressResult = await this.db.query(
        'SELECT * FROM user_progress WHERE user_id = $1',
        [userId]
      );
    }

    return {
      user: this.formatUserInfo(userResult.rows[0]),
      progress: this.formatUserProgress(progressResult.rows[0])
    };
  }

  async updateProfile(userId: string, profileData: any): Promise<any> {
    const { username, email, chess_elo, puzzle_rating, preferences } = profileData;

    // Build dynamic update query
    const updates = [];
    const values = [];
    let paramCount = 1;

    if (username !== undefined) {
      updates.push(`username = $${paramCount++}`);
      values.push(username);
    }
    if (email !== undefined) {
      updates.push(`email = $${paramCount++}`);
      values.push(email);
    }
    if (chess_elo !== undefined) {
      updates.push(`chess_elo = $${paramCount++}`);
      values.push(chess_elo);
    }
    if (puzzle_rating !== undefined) {
      updates.push(`puzzle_rating = $${paramCount++}`);
      values.push(puzzle_rating);
    }
    if (preferences !== undefined) {
      updates.push(`preferences = $${paramCount++}`);
      values.push(typeof preferences === 'string' ? preferences : JSON.stringify(preferences));
    }

    if (updates.length === 0) {
      throw new Error('No fields to update');
    }

    updates.push(`updated_at = NOW()`);
    values.push(userId); // For WHERE clause

    const query = `
      UPDATE users 
      SET ${updates.join(', ')}
      WHERE id = $${paramCount}
      RETURNING *
    `;

    const result = await this.db.query(query, values);

    if (!result.rows.length) {
      throw new Error('User not found');
    }

    return this.formatUserInfo(result.rows[0]);
  }

  async changePassword(userId: string, passwordData: any): Promise<void> {
    const { currentPassword, newPassword } = passwordData;

    // Get current user
    const result = await this.db.query(
      'SELECT password_hash FROM users WHERE id = $1',
      [userId]
    );

    if (!result.rows.length) {
      throw new Error('User not found');
    }

    // Verify current password
    const bcrypt = require('bcrypt');
    const isValidPassword = await bcrypt.compare(currentPassword, result.rows[0].password_hash);
    if (!isValidPassword) {
      throw new Error('Current password is incorrect');
    }

    // Hash new password
    const newPasswordHash = await bcrypt.hash(newPassword, 12);

    // Update password
    await this.db.query(
      'UPDATE users SET password_hash = $1, updated_at = NOW() WHERE id = $2',
      [newPasswordHash, userId]
    );
  }

  async verifyToken(token: string): Promise<any> {
    try {
      const jwt = require('jsonwebtoken');
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
      
      // Get updated user info
      const result = await this.db.query(
        'SELECT * FROM users WHERE id = $1',
        [decoded.userId]
      );

      if (!result.rows.length) {
        throw new Error('User not found');
      }

      return {
        user: this.formatUserInfo(result.rows[0]),
        tokenValid: true
      };
    } catch (error) {
      throw new Error('Invalid token');
    }
  }

  async forgotPassword(forgotData: any): Promise<void> {
    const { email } = forgotData;

    // Check if user exists
    const result = await this.db.query(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );

    if (!result.rows.length) {
      // Don't reveal if email exists or not for security
      return;
    }

    // In a real app, you would:
    // 1. Generate a reset token
    // 2. Store it in database with expiration
    // 3. Send email with reset link
    console.log(`Password reset requested for email: ${email}`);
  }

  async resetPassword(resetData: any): Promise<void> {
    const { resetToken, password } = resetData;

    // In a real app, you would:
    // 1. Verify reset token from database
    // 2. Check if token is not expired
    // 3. Update user password
    // 4. Invalidate the reset token
    
    // For now, we'll throw an error since token system isn't implemented
    throw new Error('Password reset functionality requires email service integration');
  }

  async logout(): Promise<void> {
    // JWT tokens are stateless, so logout is handled client-side
    // In a real app with token blacklisting, you would store the token
    // in a blacklist until it expires
    return;
  }

  async checkEmailAvailability(emailData: any): Promise<any> {
    const { email } = emailData;

    const result = await this.db.query(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );

    return { available: result.rows.length === 0 };
  }

  async checkUsernameAvailability(usernameData: any): Promise<any> {
    const { username } = usernameData;

    const result = await this.db.query(
      'SELECT id FROM users WHERE username = $1',
      [username]
    );

    return { available: result.rows.length === 0 };
  }

  async deleteAccount(userId: string): Promise<void> {
    // Delete user and all related data
    // This should be done in a transaction in production
    await this.db.query('DELETE FROM user_progress WHERE user_id = $1', [userId]);
    await this.db.query('DELETE FROM users WHERE id = $1', [userId]);
  }

  async healthCheck() {
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      service: 'auth'
    };
  }

  private formatUserInfo(row: any): any {
    return {
      id: row.id,
      username: row.username,
      email: row.email,
      chess_elo: row.chess_elo,
      puzzle_rating: row.puzzle_rating,
      preferences: row.preferences,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }

  private formatUserProgress(row: any): any {
    return {
      id: row.id,
      user_id: row.user_id,
      puzzles_solved: row.puzzles_solved,
      puzzles_correct: row.puzzles_correct,
      current_streak: row.current_streak,
      best_streak: row.best_streak,
      total_time_spent: row.total_time_spent,
      achievements_unlocked: row.achievements_unlocked,
      last_puzzle_date: row.last_puzzle_date,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }

  private formatAuthResponse(row: any): any {
    return {
      success: true,
      data: {
        id: row.id,
        username: row.username,
        email: row.email,
        chess_elo: row.chess_elo,
        puzzle_rating: row.puzzle_rating,
        preferences: row.preferences,
        created_at: row.created_at,
        updated_at: row.updated_at,
      }
    };
  }
}