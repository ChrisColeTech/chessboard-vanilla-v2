export interface SubscriptionResponse {
  id: string;
  user_id: string;
  plan_type: string;
  status: string;
  expires_at: string;
  created_at: string;
  updated_at: string;
}

export interface CreateSubscriptionRequest {
  user_id: string;
  plan_type: string;
  status: string;
  expires_at: string;
}

export interface UpdateSubscriptionRequest {
  user_id?: string;
  plan_type?: string;
  status?: string;
  expires_at?: string;
}