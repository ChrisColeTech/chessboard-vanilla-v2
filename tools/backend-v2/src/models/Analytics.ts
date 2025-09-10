export interface AnalyticsResponse {
  id: string;
  user_id: string;
  event_type: string;
  event_data: string;
  timestamp: string;
  session_id: string;
}

export interface CreateAnalyticsRequest {
  user_id: string;
  event_type: string;
  event_data: string;
  timestamp: string;
  session_id: string;
}

export interface UpdateAnalyticsRequest {
  user_id?: string;
  event_type?: string;
  event_data?: string;
  timestamp?: string;
  session_id?: string;
}