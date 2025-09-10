#!/usr/bin/env python3
"""
Game Method Generator
Generates game-specific service methods
"""

from base_generator import BaseMethodGenerator


class GameMethodGenerator(BaseMethodGenerator):
    """Generates game-specific service methods"""
    
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate game-specific service method"""
        
        if method_name == "getGames":
            return f'''  async {method_name}(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        elif method_name == "getGameById":
            return f'''  async {method_name}(id: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "createGame":
            return f'''  async {method_name}(gameData: any): Promise<{entity_upper}Response> {{
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (id, user_id, ai_level, user_color, current_fen, status)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *
    `, [
      id,
      gameData.user_id,
      gameData.ai_level || 1,
      gameData.user_color || 'white',
      gameData.current_fen || 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
      'active'
    ]);
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "updateGame":
            return f'''  async {method_name}(id: string, gameData: any): Promise<{entity_upper}Response> {{
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET current_fen = $1, pgn = $2, status = $3
      WHERE id = $4
      RETURNING *
    `, [
      gameData.current_fen || 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
      gameData.pgn || '',
      gameData.status || 'active',
      id
    ]);
    
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "analyzeGame":
            return f'''  async {method_name}(id: string, analysisData: any): Promise<{{analysis: string}}> {{
    // Basic game analysis implementation
    const game = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!game.rows.length) throw new Error('{entity_upper} not found');
    
    return {{ analysis: 'Game analysis not yet implemented' }};
  }}'''
        
        elif method_name == "getGameAnalysis":
            return f'''  async {method_name}(id: string): Promise<{{analysis: string}}> {{
    const game = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!game.rows.length) throw new Error('{entity_upper} not found');
    
    return {{ analysis: 'Analysis for game ' + id }};
  }}'''
        
        else:
            return self._create_stub_method(method_name, table_name, entity_upper)