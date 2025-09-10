export interface AnalysisResponse {
  id: string;
  position_fen: string;
  analysis_data: string;
  best_move: string;
  evaluation: number;
  depth: number;
  created_at: string;
}

export interface CreateAnalysisRequest {
  position_fen: string;
  analysis_data: string;
  best_move: string;
  evaluation: number;
  depth: number;
}

export interface UpdateAnalysisRequest {
  position_fen?: string;
  analysis_data?: string;
  best_move?: string;
  evaluation?: number;
  depth?: number;
}