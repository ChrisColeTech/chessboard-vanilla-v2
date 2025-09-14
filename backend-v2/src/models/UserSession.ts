export interface UserSessionResponse {
  id: string;
  user_id: string;
  refresh_token: string;
  expires_at: string;
  ip_address: string;
  user_agent: string;
  created_at: string;
  last_accessed: string;
}

export interface CreateUserSessionRequest {
  user_id: string;
  refresh_token: string;
  expires_at: string;
  ip_address: string;
  user_agent: string;
  last_accessed: string;
}

export interface UpdateUserSessionRequest {
  user_id?: string;
  refresh_token?: string;
  expires_at?: string;
  ip_address?: string;
  user_agent?: string;
  last_accessed?: string;
}