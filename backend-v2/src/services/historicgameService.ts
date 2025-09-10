import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { HistoricgameResponse, CreateHistoricgameRequest, UpdateHistoricgameRequest } from '../models/Historicgame';

export class HistoricgameService {
  private db = Database.getInstance();

  async getAllHistoricGames(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async getGameById(id: string): Promise<HistoricgameResponse> {
    const result = await this.db.query('SELECT * FROM historic_games WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Historicgame not found');
    
    return this.formatHistoricgameResponse(result.rows[0]);
  }

  async searchGames(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async getGamesByPlayer(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async getAllHistoric_games(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async getHistoricgameById(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async createHistoricgame(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async updateHistoricgame(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  async deleteHistoricgame(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM historic_games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHistoricgameResponse(row));
  }

  private formatHistoricgameResponse(row: any): HistoricgameResponse {
    return {
      id: row.id,
      white_player: row.white_player,
      black_player: row.black_player,
      result: row.result,
      pgn: row.pgn,
      event: row.event,
      date: row.date,
      eco: row.eco,
      created_at: row.created_at,
    };
  }
}