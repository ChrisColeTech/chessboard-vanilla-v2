import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { HistoricgameResponse, CreateHistoricgameRequest, UpdateHistoricgameRequest } from '../models/Historicgame';

export class HistoricgameService {
  private db = Database.getInstance();

  async getAllHistoricGames(limit: number = 50): Promise<HistoricgameResponse[]> {
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT $1', [limit]);
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async getGameById(id: string): Promise<HistoricgameResponse> {
    const result = await this.db.query('SELECT * FROM historic_games WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Historic game not found');
    
    return this.formatHistoricgameResponse(result.rows[0]);
  }

  async searchGames(searchParams?: any): Promise<HistoricgameResponse[]> {
    let query = 'SELECT * FROM historic_games';
    let params: any[] = [];
    let conditions: string[] = [];
    
    // Handle different search parameters
    if (searchParams?.player) {
      conditions.push('(white_player ILIKE $' + (params.length + 1) + ' OR black_player ILIKE $' + (params.length + 1) + ')');
      params.push(`%${searchParams.player}%`);
    }
    
    if (searchParams?.white_player) {
      conditions.push('white_player ILIKE $' + (params.length + 1));
      params.push(`%${searchParams.white_player}%`);
    }
    
    if (searchParams?.black_player) {
      conditions.push('black_player ILIKE $' + (params.length + 1));
      params.push(`%${searchParams.black_player}%`);
    }
    
    if (searchParams?.result) {
      conditions.push('result = $' + (params.length + 1));
      params.push(searchParams.result);
    }
    
    if (searchParams?.opening_eco) {
      conditions.push('opening_eco = $' + (params.length + 1));
      params.push(searchParams.opening_eco);
    }
    
    if (searchParams?.tournament_name) {
      conditions.push('tournament_name ILIKE $' + (params.length + 1));
      params.push(`%${searchParams.tournament_name}%`);
    }
    
    if (searchParams?.year) {
      conditions.push('tournament_year = $' + (params.length + 1));
      params.push(parseInt(searchParams.year));
    }
    
    // Add WHERE clause if there are conditions
    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    
    query += ' ORDER BY created_at DESC LIMIT 50';
    
    const result = await this.db.query(query, params);
    
    // Return empty array instead of throwing error when no results found
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async getGamesByPlayer(playerName: string): Promise<HistoricgameResponse[]> {
    const result = await this.db.query(`
      SELECT * FROM historic_games 
      WHERE white_player ILIKE $1 OR black_player ILIKE $1 
      ORDER BY created_at DESC LIMIT 50
    `, [`%${playerName}%`]);
    
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async getAllHistoric_games(limit: number = 50): Promise<HistoricgameResponse[]> {
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT $1', [limit]);
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async getHistoricgameById(id: string): Promise<HistoricgameResponse> {
    const result = await this.db.query('SELECT * FROM historic_games WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Historic game not found');
    
    return this.formatHistoricgameResponse(result.rows[0]);
  }

  async createHistoricgame(data: CreateHistoricgameRequest): Promise<HistoricgameResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO historic_games (
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
    
    return this.formatHistoricgameResponse(result.rows[0]);
  }

  async updateHistoricgame(id: string, data: UpdateHistoricgameRequest): Promise<HistoricgameResponse> {
    const result = await this.db.query(`
      UPDATE historic_games 
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
    return this.formatHistoricgameResponse(result.rows[0]);
  }

  async deleteHistoricgame(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM historic_games WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Historic game not found');
  }

  private formatHistoricgameResponse(row: any): HistoricgameResponse {
    return {
      id: row.id,
      white_player: row.white_player,
      black_player: row.black_player,
      white_rating: row.white_rating,
      black_rating: row.black_rating,
      result: row.result,
      pgn: row.pgn,
      event: row.event,
      date: row.date,
      eco: row.eco,
      tournament_name: row.tournament_name,
      tournament_year: row.tournament_year,
      opening_name: row.opening_name,
      opening_eco: row.opening_eco,
      created_at: row.created_at,
    };
  }
}