#!/usr/bin/env python3
"""
Puzzle Method Generator
Generates puzzle-specific service methods
"""

from base_generator import BaseMethodGenerator


class PuzzleMethodGenerator(BaseMethodGenerator):
    """Generates puzzle-specific service methods"""
    
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate puzzle-specific service method"""
        
        if method_name == "getNextPuzzle":
            return f'''  async {method_name}(userId: string): Promise<{entity_upper}Response> {{
    // Get next puzzle for user based on rating and history
    const result = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE rating BETWEEN $1 AND $2 
      ORDER BY RANDOM() 
      LIMIT 1
    `, [800, 2000]);
    
    if (!result.rows.length) {{
      throw new Error('No puzzles available');
    }}
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "solvePuzzle":
            return f'''  async {method_name}(puzzleId: string, solutionData: any): Promise<{{correct: boolean, solution?: string[]}}> {{
    const puzzle = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [puzzleId]);
    if (!puzzle.rows.length) throw new Error('{entity_upper} not found');
    
    const puzzleData = puzzle.rows[0];
    const userMoves = solutionData.moves || [];
    const solutionMoves = JSON.parse(puzzleData.solution_moves || '[]');
    
    const isCorrect = JSON.stringify(userMoves) === JSON.stringify(solutionMoves);
    
    return {{
      correct: isCorrect,
      solution: isCorrect ? undefined : solutionMoves
    }};
  }}'''
        
        elif method_name == "getPuzzleHint":
            return f'''  async {method_name}(puzzleId: string): Promise<{{hint: string}}> {{
    const puzzle = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [puzzleId]);
    if (!puzzle.rows.length) throw new Error('{entity_upper} not found');
    
    const themes = JSON.parse(puzzle.rows[0].themes || '[]');
    const hint = themes.length > 0 ? `Look for ${{themes[0]}} tactics` : 'Look for the best move';
    
    return {{ hint }};
  }}'''
        
        elif method_name == "getPuzzleCategories":
            return f'''  async {method_name}(): Promise<string[]> {{
    const result = await this.db.query(`
      SELECT DISTINCT themes FROM {table_name} 
      WHERE themes IS NOT NULL AND themes != ''
      LIMIT 50
    `);
    
    const allThemes = new Set<string>();
    result.rows.forEach(row => {{
      try {{
        const themes = JSON.parse(row.themes || '[]');
        themes.forEach((theme: string) => allThemes.add(theme));
      }} catch (e) {{
        // Skip invalid JSON
      }}
    }});
    
    return Array.from(allThemes).slice(0, 20);
  }}'''
        
        elif method_name == "getPuzzleHistory":
            return f'''  async {method_name}(userId: string): Promise<any[]> {{
    // Return empty array for now - would need puzzle_attempts table
    return [];
  }}'''
        
        elif method_name == "createCustomPuzzle":
            return f'''  async {method_name}(puzzleData: any): Promise<{entity_upper}Response> {{
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (id, fen, solution_moves, themes, rating, description)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *
    `, [
      id,
      puzzleData.fen,
      JSON.stringify(puzzleData.solutionMoves || []),
      JSON.stringify(puzzleData.themes || []),
      puzzleData.rating || 1000,
      puzzleData.description || ''
    ]);
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "getCustomPuzzles":
            return f'''  async {method_name}(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE description LIKE '%custom%' 
      ORDER BY created_at DESC 
      LIMIT 20
    `);
    
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        else:
            return self._create_stub_method(method_name)