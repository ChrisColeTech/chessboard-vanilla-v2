#!/usr/bin/env python3
"""
User Method Generator
Generates user-specific service methods
"""

from base_generator import BaseMethodGenerator


class UserMethodGenerator(BaseMethodGenerator):
    """Generates user-specific service methods"""
    
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate user-specific service method"""
        
        if method_name == "getUserProfile":
            return f'''  async {method_name}(userId: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [userId]);
    if (!result.rows.length) throw new Error('User not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "updateUserProfile":
            return f'''  async {method_name}(userId: string, profileData: any): Promise<{entity_upper}Response> {{
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET chess_elo = $1, puzzle_rating = $2, updated_at = NOW()
      WHERE id = $3
      RETURNING *
    `, [
      profileData.chess_elo,
      profileData.puzzle_rating,
      userId
    ]);
    
    if (!result.rows.length) throw new Error('User not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "getUserPreferences":
            return f'''  async {method_name}(userId: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [userId]);
    if (!result.rows.length) throw new Error('User not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "updateUserPreferences":
            return f'''  async {method_name}(userId: string, preferencesData: any): Promise<{entity_upper}Response> {{
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET preferences = $1, updated_at = NOW()
      WHERE id = $2
      RETURNING *
    `, [
      JSON.stringify(preferencesData),
      userId
    ]);
    
    if (!result.rows.length) throw new Error('User not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "getUserSettings":
            return f'''  async {method_name}(userId: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [userId]);
    if (!result.rows.length) throw new Error('User not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "updateUserSettings":
            return f'''  async {method_name}(userId: string, settingsData: any): Promise<{entity_upper}Response> {{
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET chess_elo = $1, puzzle_rating = $2, updated_at = NOW()
      WHERE id = $3
      RETURNING *
    `, [
      settingsData.chess_elo,
      settingsData.puzzle_rating,
      userId
    ]);
    
    if (!result.rows.length) throw new Error('User not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        else:
            return self._create_stub_method(method_name, table_name, entity_upper)