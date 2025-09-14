// Generated types for UserSession

export interface UserSession {
  id: string;
  user_id: string;
  refresh_token: string;
  expires_at: string;
  ip_address: string;
  user_agent: string;
  created_at: string;
  last_accessed: string;
}

export interface UserSessionCreate {
  // Properties needed for creating new UserSession
  id: string;
  user_id: string;
  refresh_token: string;
  expires_at: string;
  ip_address: string;
  user_agent: string;
  created_at: string;
  last_accessed: string;
}

export interface UserSessionUpdate {
  // Properties that can be updated
  id: string;
  user_id: string;
  refresh_token: string;
  expires_at: string;
  ip_address: string;
  user_agent: string;
  created_at: string;
  last_accessed: string;
}

export interface UserSessionFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
