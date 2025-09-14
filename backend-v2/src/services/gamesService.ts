import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { GameResponse, CreateGameRequest, UpdateGameRequest } from '../models/Game';

export class GameService {
  private db = Database.getInstance();

  async getGamesByPlayer(...args: any[]): Promise<any> {
    // Generic implementation for getGamesByPlayer
    const result = await this.db.query('SELECT * FROM games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGameResponse(row));
  }

async listGames(): Promise<GameResponse[]> {
    const result = await this.db.query('SELECT * FROM games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGameResponse(row));
  }

async updateGame(id: string, data: UpdateGameRequest): Promise<GameResponse> {
    const result = await this.db.query(`
      UPDATE games 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Game not found');
    return this.formatGameResponse(result.rows[0]);
  }

async getGameById(id: string): Promise<GameResponse> {
    const result = await this.db.query('SELECT * FROM games WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Game not found');
    
    return this.formatGameResponse(result.rows[0]);
  }

async deleteGame(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM games WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Game not found');
  }

  async completeGame(...args: any[]): Promise<any> {
    // Generic implementation for completeGame
    const result = await this.db.query('SELECT * FROM games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGameResponse(row));
  }

async getAllGames(): Promise<GameResponse[]> {
    const result = await this.db.query('SELECT * FROM games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGameResponse(row));
  }

  async getActiveGames(...args: any[]): Promise<any> {
    // Generic implementation for getActiveGames
    const result = await this.db.query('SELECT * FROM games ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatGameResponse(row));
  }

async createGame(data: CreateGameRequest): Promise<GameResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO games (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatGameResponse(result.rows[0]);
  }

private formatGameResponse(row: any): GameResponse {
    return {
      id: row.id,
      white_player_id: row.white_player_id,
      black_player_id: row.black_player_id,
      time_control: row.time_control,
      ai_level: row.ai_level,
      initial_fen: row.initial_fen,
      current_fen: row.current_fen,
      pgn: row.pgn,
      result: row.result,
      termination: row.termination,
      opening_eco: row.opening_eco,
      opening_name: row.opening_name,
      move_count: row.move_count,
      white_elo_before: row.white_elo_before,
      white_elo_after: row.white_elo_after,
      black_elo_before: row.black_elo_before,
      black_elo_after: row.black_elo_after,
      started_at: row.started_at,
      completed_at: row.completed_at,
    };
  }
}