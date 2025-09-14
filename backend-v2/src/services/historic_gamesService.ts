import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { HistoricGameResponse, CreateHistoricGameRequest, UpdateHistoricGameRequest } from '../models/HistoricGame';

export class HistoricGameService {
  private db = Database.getInstance();

async deleteHistoricGame(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM historic_games WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('HistoricGame not found');
  }

  async searchHistoricGames(...args: any[]): Promise<any> {
    // Generic implementation for searchHistoricGames
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricGameResponse(row));
  }

async getHistoricGameById(id: string): Promise<HistoricGameResponse> {
    const result = await this.db.query('SELECT * FROM historic_games WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('HistoricGame not found');
    
    return this.formatHistoricGameResponse(result.rows[0]);
  }

  async getHistoricGamesByPlayer(...args: any[]): Promise<any> {
    // Generic implementation for getHistoricGamesByPlayer
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricGameResponse(row));
  }

async listHistoricGames(): Promise<HistoricGameResponse[]> {
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricGameResponse(row));
  }

async createHistoricGame(data: CreateHistoricGameRequest): Promise<HistoricGameResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO historic_games (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatHistoricGameResponse(result.rows[0]);
  }

async updateHistoricGame(id: string, data: UpdateHistoricGameRequest): Promise<HistoricGameResponse> {
    const result = await this.db.query(`
      UPDATE historic_games 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('HistoricGame not found');
    return this.formatHistoricGameResponse(result.rows[0]);
  }

async getAllHistoric_games(): Promise<HistoricGameResponse[]> {
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricGameResponse(row));
  }

  async getHistoricGamesByTournament(...args: any[]): Promise<any> {
    // Generic implementation for getHistoricGamesByTournament
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricGameResponse(row));
  }

private formatHistoricGameResponse(row: any): HistoricGameResponse {
    return {
      id: row.id,
      white_player: row.white_player,
      black_player: row.black_player,
      white_rating: row.white_rating,
      black_rating: row.black_rating,
      tournament_name: row.tournament_name,
      tournament_year: row.tournament_year,
      round_info: row.round_info,
      pgn: row.pgn,
      result: row.result,
      opening_eco: row.opening_eco,
      opening_name: row.opening_name,
      game_significance: row.game_significance,
      key_moments: row.key_moments,
      game_date: row.game_date,
      created_at: row.created_at,
    };
  }
}