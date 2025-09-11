#!/usr/bin/env python3
"""
Auth Method Generator
Generates authentication-specific service methods
"""

from base_generator import BaseMethodGenerator


class AuthMethodGenerator(BaseMethodGenerator):
    """Generates authentication-specific service methods"""
    
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate auth-specific service method"""
        
        if method_name == "register":
            return f'''  async {method_name}(registerData: any): Promise<any> {{
    const {{ username, email, password }} = registerData;

    // Check if user already exists
    const existingUser = await this.db.query(
      'SELECT id FROM {table_name} WHERE email = $1 OR username = $2',
      [email, username]
    );

    if (existingUser.rows.length > 0) {{
      throw new Error('User with this email or username already exists');
    }}

    // Hash password
    const bcrypt = require('bcrypt');
    const passwordHash = await bcrypt.hash(password, 12);

    // Create user
    const userId = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (id, username, email, password_hash, chess_elo, puzzle_rating, preferences, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
      RETURNING *
    `, [userId, username, email, passwordHash, 1000, 1000, '{{}}']);

    if (!result.rows.length) {{
      throw new Error('Failed to create user');
    }}

    return this.formatUserInfo(result.rows[0]);
  }}'''

        elif method_name == "login":
            return f'''  async {method_name}(loginData: any): Promise<any> {{
    const {{ email, password }} = loginData;

    // Find user by email
    const result = await this.db.query(
      'SELECT * FROM {table_name} WHERE email = $1',
      [email]
    );

    if (!result.rows.length) {{
      throw new Error('Invalid credentials');
    }}

    const user = result.rows[0];

    // Verify password
    const bcrypt = require('bcrypt');
    const isValidPassword = await bcrypt.compare(password, user.password_hash);
    if (!isValidPassword) {{
      throw new Error('Invalid credentials');
    }}

    // Generate JWT token
    const jwt = require('jsonwebtoken');
    const token = jwt.sign(
      {{ 
        id: user.id, 
        email: user.email,
        username: user.username 
      }},
      process.env.JWT_SECRET!,
      {{ expiresIn: '7d' }}
    );

    return {{
      user: this.formatUserInfo(user),
      token
    }};
  }}'''

        elif method_name == "getCurrentUser":
            return f'''  async {method_name}(userId: string): Promise<any> {{
    // Get user info
    const userResult = await this.db.query(
      'SELECT * FROM {table_name} WHERE id = $1',
      [userId]
    );

    if (!userResult.rows.length) {{
      throw new Error('User not found');
    }}

    // Get user progress (or create default if doesn't exist)
    let progressResult = await this.db.query(
      'SELECT * FROM user_progress WHERE user_id = $1',
      [userId]
    );

    // If no progress exists, create default progress
    if (!progressResult.rows.length) {{
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
    }}

    return {{
      user: this.formatUserInfo(userResult.rows[0]),
      progress: this.formatUserProgress(progressResult.rows[0])
    }};
  }}'''

        elif method_name == "updateProfile":
            return f'''  async {method_name}(userId: string, profileData: any): Promise<any> {{
    const {{ username, email, chess_elo, puzzle_rating, preferences }} = profileData;

    // Build dynamic update query
    const updates = [];
    const values = [];
    let paramCount = 1;

    if (username !== undefined) {{
      updates.push(`username = $${{paramCount++}}`);
      values.push(username);
    }}
    if (email !== undefined) {{
      updates.push(`email = $${{paramCount++}}`);
      values.push(email);
    }}
    if (chess_elo !== undefined) {{
      updates.push(`chess_elo = $${{paramCount++}}`);
      values.push(chess_elo);
    }}
    if (puzzle_rating !== undefined) {{
      updates.push(`puzzle_rating = $${{paramCount++}}`);
      values.push(puzzle_rating);
    }}
    if (preferences !== undefined) {{
      updates.push(`preferences = $${{paramCount++}}`);
      values.push(typeof preferences === 'string' ? preferences : JSON.stringify(preferences));
    }}

    if (updates.length === 0) {{
      throw new Error('No fields to update');
    }}

    updates.push(`updated_at = NOW()`);
    values.push(userId); // For WHERE clause

    const query = `
      UPDATE {table_name} 
      SET ${{updates.join(', ')}}
      WHERE id = $${{paramCount}}
      RETURNING *
    `;

    // First try to update existing profile
    let result = await this.db.query(query, values);

    // If no profile exists, create one
    if (!result.rows.length) {{
      const profileId = require('uuid').v4();
      result = await this.db.query(`
        INSERT INTO {table_name} (id, username, email, chess_elo, puzzle_rating, preferences, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
        RETURNING *
      `, [profileId, username, email, chess_elo, puzzle_rating, typeof preferences === 'string' ? preferences : JSON.stringify(preferences)]);
    }}

    return this.formatUserInfo(result.rows[0]);
  }}'''

        elif method_name == "changePassword":
            return f'''  async {method_name}(userId: string, passwordData: any): Promise<void> {{
    const {{ currentPassword, newPassword }} = passwordData;

    // Get current user
    const result = await this.db.query(
      'SELECT password_hash FROM {table_name} WHERE id = $1',
      [userId]
    );

    if (!result.rows.length) {{
      throw new Error('User not found');
    }}

    // Verify current password
    const bcrypt = require('bcrypt');
    const isValidPassword = await bcrypt.compare(currentPassword, result.rows[0].password_hash);
    if (!isValidPassword) {{
      throw new Error('Current password is incorrect');
    }}

    // Hash new password
    const newPasswordHash = await bcrypt.hash(newPassword, 12);

    // Update password
    await this.db.query(
      'UPDATE {table_name} SET password_hash = $1, updated_at = NOW() WHERE id = $2',
      [newPasswordHash, userId]
    );
  }}'''

        elif method_name == "verifyToken":
            return f'''  async {method_name}(token: string): Promise<any> {{
    try {{
      const jwt = require('jsonwebtoken');
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
      
      // Get updated user info
      const result = await this.db.query(
        'SELECT * FROM {table_name} WHERE id = $1',
        [decoded.id]
      );

      if (!result.rows.length) {{
        throw new Error('User not found');
      }}

      return {{
        user: this.formatUserInfo(result.rows[0]),
        tokenValid: true
      }};
    }} catch (error) {{
      throw new Error('Invalid token');
    }}
  }}'''

        elif method_name == "forgotPassword":
            return f'''  async {method_name}(forgotData: any): Promise<void> {{
    const {{ email }} = forgotData;

    // Check if user exists
    const result = await this.db.query(
      'SELECT id FROM {table_name} WHERE email = $1',
      [email]
    );

    if (!result.rows.length) {{
      // Don't reveal if email exists or not for security
      return;
    }}

    // In a real app, you would:
    // 1. Generate a reset token
    // 2. Store it in database with expiration
    // 3. Send email with reset link
    console.log(`Password reset requested for email: ${{email}}`);
  }}'''

        elif method_name == "resetPassword":
            return f'''  async {method_name}(resetData: any): Promise<void> {{
    const {{ email, username, currentPassword, newPassword }} = resetData;

    // Find user by email or username
    let query = 'SELECT * FROM {table_name} WHERE ';
    let params = [];
    
    if (email) {{
      query += 'email = $1';
      params.push(email);
    }} else if (username) {{
      query += 'username = $1';
      params.push(username);
    }} else {{
      throw new Error('Email or username is required');
    }}

    const result = await this.db.query(query, params);

    if (!result.rows.length) {{
      throw new Error('User not found');
    }}

    const user = result.rows[0];

    // Verify current password
    const bcrypt = require('bcrypt');
    const isValidPassword = await bcrypt.compare(currentPassword, user.password_hash);
    if (!isValidPassword) {{
      throw new Error('Current password is incorrect');
    }}

    // Hash new password
    const newPasswordHash = await bcrypt.hash(newPassword, 12);

    // Update password
    await this.db.query(
      'UPDATE {table_name} SET password_hash = $1, updated_at = NOW() WHERE id = $2',
      [newPasswordHash, user.id]
    );
  }}'''

        elif method_name == "logout":
            return f'''  async {method_name}(): Promise<void> {{
    // JWT tokens are stateless, so logout is handled client-side
    // In a real app with token blacklisting, you would store the token
    // in a blacklist until it expires
    return;
  }}'''

        elif method_name == "checkEmailAvailability":
            return f'''  async {method_name}(emailData: any): Promise<any> {{
    const {{ email }} = emailData;

    const result = await this.db.query(
      'SELECT id FROM {table_name} WHERE email = $1',
      [email]
    );

    return {{ available: result.rows.length === 0 }};
  }}'''

        elif method_name == "checkUsernameAvailability":
            return f'''  async {method_name}(usernameData: any): Promise<any> {{
    const {{ username }} = usernameData;

    const result = await this.db.query(
      'SELECT id FROM {table_name} WHERE username = $1',
      [username]
    );

    return {{ available: result.rows.length === 0 }};
  }}'''

        elif method_name == "deleteAccount":
            return f'''  async {method_name}(userId: string): Promise<void> {{
    // Delete user and all related data
    // This should be done in a transaction in production
    await this.db.query('DELETE FROM user_progress WHERE user_id = $1', [userId]);
    await this.db.query('DELETE FROM {table_name} WHERE id = $1', [userId]);
  }}'''

        elif method_name == "healthCheck":
            return f'''  async {method_name}() {{
    return {{
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      service: 'auth'
    }};
  }}'''
        
        else:
            return self._create_stub_method(method_name, table_name, entity_upper)