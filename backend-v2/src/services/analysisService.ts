import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { AnalysisResponse, CreateAnalysisRequest, UpdateAnalysisRequest } from '../models/Analysis';

export class AnalysisService {
  private db = Database.getInstance();

  async analyzePosition(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM analysis_positions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAnalysisResponse(row));
  }

  async getPositionAnalysis(): Promise<AnalysisResponse[]> {
    const result = await this.db.query('SELECT * FROM analysis_positions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAnalysisResponse(row));
  }

  async saveAnalysis(...args: any[]): Promise<any> {
    // Analysis functionality would require external chess engine
    return { message: "Analysis functionality requires chess engine integration" };
  }

  async getBestMove(): Promise<AnalysisResponse[]> {
    const result = await this.db.query('SELECT * FROM analysis_positions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAnalysisResponse(row));
  }

  async getAllAnalysis(): Promise<AnalysisResponse[]> {
    const result = await this.db.query('SELECT * FROM analysis_positions ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAnalysisResponse(row));
  }

  async getAnalysisById(id: string): Promise<AnalysisResponse> {
    const result = await this.db.query('SELECT * FROM analysis_positions WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Analysis not found');
    
    return this.formatAnalysisResponse(result.rows[0]);
  }

  async createAnalysis(data: CreateAnalysisRequest): Promise<AnalysisResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO analysis_positions (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatAnalysisResponse(result.rows[0]);
  }

  async updateAnalysis(id: string, data: UpdateAnalysisRequest): Promise<AnalysisResponse> {
    const result = await this.db.query(`
      UPDATE analysis_positions 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Analysis not found');
    return this.formatAnalysisResponse(result.rows[0]);
  }

  async deleteAnalysis(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM analysis_positions WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Analysis not found');
  }

  private formatAnalysisResponse(row: any): AnalysisResponse {
    return {
      id: row.id,
      position_fen: row.position_fen,
      analysis_data: row.analysis_data,
      best_move: row.best_move,
      evaluation: row.evaluation,
      depth: row.depth,
      created_at: row.created_at,
    };
  }
}