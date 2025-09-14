// Generated types for Auth

export interface Auth {
  id: string;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface AuthCreate {
  // Properties needed for creating new Auth
  id: string;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface AuthUpdate {
  // Properties that can be updated
  id: string;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface AuthFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
