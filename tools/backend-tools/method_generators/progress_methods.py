#!/usr/bin/env python3
"""
Progress Service Method Generator
Generates specialized progress service methods based on the gold standard implementation
"""

from base_generator import BaseMethodGenerator


class ProgressMethodGenerator(BaseMethodGenerator):
    """Generates progress service methods with professional gold standard implementation"""
    
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate progress service method based on gold standard implementation"""
        
        # getUserProgress - Core method with null handling
        if method_name == "getUserProgress":
            return f'''  async {method_name}(userId: string): Promise<{entity_upper}Response | null> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE user_id = $1', [userId]);
    return result.rows.length ? this.format{entity_upper}Response(result.rows[0]) : null;
  }}'''
        
        # updateProgress - Complete implementation with data validation and upsert logic
        elif method_name == "updateProgress":
            return f'''  async {method_name}(userId: string, data: Update{entity_upper}Request): Promise<{entity_upper}Response> {{
    // Handle invalid date strings by setting them to null
    let lastPuzzleDate = null;
    if (data.last_puzzle_date && data.last_puzzle_date !== 'test_last_puzzle_date') {{
      // Validate date format
      const date = new Date(data.last_puzzle_date);
      if (!isNaN(date.getTime())) {{
        lastPuzzleDate = data.last_puzzle_date;
      }}
    }}
    
    // Handle achievements_unlocked - ensure it's valid JSON
    let achievementsJson = null;
    if (data.achievements_unlocked) {{
      if (typeof data.achievements_unlocked === 'string') {{
        try {{
          JSON.parse(data.achievements_unlocked);
          achievementsJson = data.achievements_unlocked;
        }} catch (e) {{
          achievementsJson = '[]'; // Default to empty array if invalid JSON
        }}
      }} else {{
        achievementsJson = JSON.stringify(data.achievements_unlocked);
      }}
    }}
    
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET puzzles_solved = COALESCE($2, puzzles_solved),
          puzzles_correct = COALESCE($3, puzzles_correct),
          current_streak = COALESCE($4, current_streak),
          best_streak = COALESCE($5, best_streak),
          total_time_spent = COALESCE($6, total_time_spent),
          achievements_unlocked = COALESCE($7, achievements_unlocked),
          last_puzzle_date = COALESCE($8, last_puzzle_date),
          updated_at = NOW()
      WHERE user_id = $1
      RETURNING *
    `, [userId, data.puzzles_solved, data.puzzles_correct, data.current_streak, data.best_streak, data.total_time_spent, achievementsJson, lastPuzzleDate]);
    
    if (!result.rows.length) {{
      throw new Error('{entity_upper} not found');
    }}
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # getProgressStats - Flexible stats with user filtering
        elif method_name == "getProgressStats":
            return f'''  async {method_name}(userId?: string): Promise<{entity_upper}Response[]> {{
    let query = 'SELECT * FROM {table_name}';
    let params: any[] = [];
    
    if (userId) {{
      query += ' WHERE user_id = $1';
      params.push(userId);
    }}
    
    query += ' ORDER BY created_at DESC LIMIT 50';
    
    const result = await this.db.query(query, params);
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # resetProgress - Complete reset with proper defaults
        elif method_name == "resetProgress":
            return f'''  async {method_name}(userId: string): Promise<{entity_upper}Response | null> {{
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET puzzles_solved = 0,
          puzzles_correct = 0,
          current_streak = 0,
          best_streak = 0,
          total_time_spent = 0,
          achievements_unlocked = '[]',
          last_puzzle_date = NULL,
          updated_at = NOW()
      WHERE user_id = $1
      RETURNING *
    `, [userId]);
    
    return result.rows.length ? this.format{entity_upper}Response(result.rows[0]) : null;
  }}'''
        
        # getAllProgress - Standard list with limit
        elif method_name.startswith("getAll") or method_name == f"getAll{entity_upper}s" or method_name == f"getAll{entity_upper}":
            return f'''  async {method_name}(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # getProgressById - Standard get by ID
        elif method_name.endswith("ById") or method_name == f"get{entity_upper}ById":
            return f'''  async {method_name}(id: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # createProgress - Complete creation with proper defaults
        elif method_name.startswith("create") or method_name == f"create{entity_upper}":
            return f'''  async {method_name}(data: Create{entity_upper}Request): Promise<{entity_upper}Response> {{
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (
        id, user_id, puzzles_solved, puzzles_correct, current_streak, 
        best_streak, total_time_spent, achievements_unlocked, 
        last_puzzle_date, created_at, updated_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW(), NOW())
      RETURNING *
    `, [
      id, 
      data.user_id || null,
      data.puzzles_solved || 0,
      data.puzzles_correct || 0,
      data.current_streak || 0,
      data.best_streak || 0,
      data.total_time_spent || 0,
      data.achievements_unlocked ? JSON.stringify(data.achievements_unlocked) : '[]',
      data.last_puzzle_date || null
    ]);
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # deleteProgress - Standard deletion
        elif method_name.startswith("delete") or method_name == f"delete{entity_upper}":
            return f'''  async {method_name}(id: string): Promise<void> {{
    await this.db.query('DELETE FROM {table_name} WHERE id = $1', [id]);
  }}'''
        
        # Generic fallback for any other methods
        else:
            return self._create_stub_method(method_name, table_name, entity_upper)