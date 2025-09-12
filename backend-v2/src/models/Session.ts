export interface SessionResponse {
  id: string;
  user_id: string;
  refresh_token: string;
  session_token: string;
  expires_at: string;
  created_at: string;
  last_accessed: string;
}

export interface CreateSessionRequest {
  user_id: string;
  refresh_token: string;
  session_token: string;
  expires_at: string;
  last_accessed: string;
}

export interface UpdateSessionRequest {
  user_id?: string;
  refresh_token?: string;
  session_token?: string;
  expires_at?: string;
  last_accessed?: string;
}