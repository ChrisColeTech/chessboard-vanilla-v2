#!/usr/bin/env python3
"""
Historic Game Service Method Generator
Generates specialized historic game service methods based on the gold standard implementation
"""

from base_generator import BaseMethodGenerator


class HistoricgameMethodGenerator(BaseMethodGenerator):
    """Generates historic game service methods with professional gold standard implementation including advanced search"""
    
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate historic game service method based on gold standard implementation"""
        
        # getAllHistoricGames - Flexible listing with configurable limit
        if method_name.startswith("getAll") or method_name == f"getAll{entity_upper}s" or method_name == f"getAll{entity_upper}":
            return f'''  async {method_name}(limit: number = 50): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT $1', [limit]);
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # getGameById - Standard get by ID
        elif method_name.endswith("ById") or method_name == f"get{entity_upper}ById" or method_name == "getGameById":
            return f'''  async {method_name}(id: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Historic game not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # searchGames - Advanced search functionality with multiple parameters
        elif method_name == "searchGames":
            return f'''  async {method_name}(searchParams?: any): Promise<{entity_upper}Response[]> {{
    let query = 'SELECT * FROM {table_name}';
    let params: any[] = [];
    let conditions: string[] = [];
    
    // Handle different search parameters
    if (searchParams?.player) {{
      conditions.push('(white_player ILIKE $' + (params.length + 1) + ' OR black_player ILIKE $' + (params.length + 1) + ')');
      params.push(`%${{searchParams.player}}%`);
    }}
    
    if (searchParams?.white_player) {{
      conditions.push('white_player ILIKE $' + (params.length + 1));
      params.push(`%${{searchParams.white_player}}%`);
    }}
    
    if (searchParams?.black_player) {{
      conditions.push('black_player ILIKE $' + (params.length + 1));
      params.push(`%${{searchParams.black_player}}%`);
    }}
    
    if (searchParams?.result) {{
      conditions.push('result = $' + (params.length + 1));
      params.push(searchParams.result);
    }}
    
    if (searchParams?.opening_eco) {{
      conditions.push('opening_eco = $' + (params.length + 1));
      params.push(searchParams.opening_eco);
    }}
    
    if (searchParams?.tournament_name) {{
      conditions.push('tournament_name ILIKE $' + (params.length + 1));
      params.push(`%${{searchParams.tournament_name}}%`);
    }}
    
    if (searchParams?.year) {{
      conditions.push('tournament_year = $' + (params.length + 1));
      params.push(parseInt(searchParams.year));
    }}
    
    // Add WHERE clause if there are conditions
    if (conditions.length > 0) {{
      query += ' WHERE ' + conditions.join(' AND ');
    }}
    
    query += ' ORDER BY created_at DESC LIMIT 50';
    
    const result = await this.db.query(query, params);
    
    // Return empty array instead of throwing error when no results found
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # getGamesByPlayer - Player-specific search
        elif method_name == "getGamesByPlayer":
            return f'''  async {method_name}(playerName: string): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE white_player ILIKE $1 OR black_player ILIKE $1 
      ORDER BY created_at DESC LIMIT 50
    `, [`%${{playerName}}%`]);
    
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # getGamesByResult - Result-specific filtering
        elif method_name == "getGamesByResult":
            return f'''  async {method_name}(result: string): Promise<{entity_upper}Response[]> {{
    const queryResult = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE result = $1 
      ORDER BY created_at DESC LIMIT 50
    `, [result]);
    
    return queryResult.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # getGamesByOpening - Opening-specific filtering
        elif method_name == "getGamesByOpening":
            return f'''  async {method_name}(ecoCode: string): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE opening_eco = $1 
      ORDER BY created_at DESC LIMIT 50
    `, [ecoCode]);
    
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # getGamesByTournament - Tournament-specific filtering
        elif method_name == "getGamesByTournament":
            return f'''  async {method_name}(tournamentName: string): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE tournament_name ILIKE $1 
      ORDER BY created_at DESC LIMIT 50
    `, [`%${{tournamentName}}%`]);
    
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # getGamesByYear - Year-specific filtering
        elif method_name == "getGamesByYear":
            return f'''  async {method_name}(year: number): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE tournament_year = $1 
      ORDER BY created_at DESC LIMIT 50
    `, [year]);
    
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # createHistoricgame - Complete creation with proper defaults
        elif method_name.startswith("create") or method_name == f"create{entity_upper}":
            return f'''  async {method_name}(data: Create{entity_upper}Request): Promise<{entity_upper}Response> {{
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (
        id, white_player, black_player, white_rating, black_rating,
        tournament_name, tournament_year, opening_name, opening_eco,
        result, pgn, created_at, updated_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, NOW(), NOW())
      RETURNING *
    `, [
      id,
      data.white_player || 'Unknown',
      data.black_player || 'Unknown',
      data.white_rating || null,
      data.black_rating || null,
      data.tournament_name || null,
      data.tournament_year || null,
      data.opening_name || null,
      data.opening_eco || null,
      data.result || '*',
      data.pgn || ''
    ]);
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # updateHistoricgame - Complete update with COALESCE pattern
        elif method_name.startswith("update") or method_name == f"update{entity_upper}":
            return f'''  async {method_name}(id: string, data: Update{entity_upper}Request): Promise<{entity_upper}Response> {{
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET white_player = COALESCE($2, white_player),
          black_player = COALESCE($3, black_player),
          white_rating = COALESCE($4, white_rating),
          black_rating = COALESCE($5, black_rating),
          tournament_name = COALESCE($6, tournament_name),
          tournament_year = COALESCE($7, tournament_year),
          opening_name = COALESCE($8, opening_name),
          opening_eco = COALESCE($9, opening_eco),
          result = COALESCE($10, result),
          pgn = COALESCE($11, pgn),
          updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [
      id,
      data.white_player,
      data.black_player,
      data.white_rating,
      data.black_rating,
      data.tournament_name,
      data.tournament_year,
      data.opening_name,
      data.opening_eco,
      data.result,
      data.pgn
    ]);
    
    if (!result.rows.length) throw new Error('Historic game not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # deleteHistoricgame - Enhanced deletion with row count check
        elif method_name.startswith("delete") or method_name == f"delete{entity_upper}":
            return f'''  async {method_name}(id: string): Promise<void> {{
    const result = await this.db.query('DELETE FROM {table_name} WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Historic game not found');
  }}'''
        
        # getRandomGame - Random game selection
        elif method_name == "getRandomGame":
            return f'''  async {method_name}(): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1');
    if (!result.rows.length) throw new Error('No historic games found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # getGameStats - Statistical aggregation
        elif method_name == "getGameStats":
            return f'''  async {method_name}(): Promise<any> {{
    const totalGames = await this.db.query('SELECT COUNT(*) as total FROM {table_name}');
    const whiteWins = await this.db.query('SELECT COUNT(*) as wins FROM {table_name} WHERE result = \\'1-0\\'');
    const blackWins = await this.db.query('SELECT COUNT(*) as wins FROM {table_name} WHERE result = \\'0-1\\'');
    const draws = await this.db.query('SELECT COUNT(*) as draws FROM {table_name} WHERE result = \\'1/2-1/2\\'');
    
    return {{
      total_games: parseInt(totalGames.rows[0].total),
      white_wins: parseInt(whiteWins.rows[0].wins),
      black_wins: parseInt(blackWins.rows[0].wins),
      draws: parseInt(draws.rows[0].draws)
    }};
  }}'''
        
        # Generic fallback for any other methods
        else:
            return self._create_stub_method(method_name, table_name, entity_upper)