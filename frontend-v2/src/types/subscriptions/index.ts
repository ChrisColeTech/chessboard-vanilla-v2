// Subscriptions Domain Types

import type { DomainState } from '../common';

// Subscription types from backend
export interface Subscription {
  id: string;
  user_id: string;
  plan_type: string;
  status: string;
  expires_at: string;
  created_at: string;
  updated_at: string;
}

// Response type (same as base entity)
export type SubscriptionResponse = Subscription;

// Create request omits auto-generated fields
export type CreateSubscriptionRequest = Omit<Subscription, 'id' | 'created_at' | 'updated_at'>;

// Update request makes create fields optional
export type UpdateSubscriptionRequest = Partial<CreateSubscriptionRequest>;

// Frontend-specific subscriptions types
// Uses common DomainState interface from ../common
export type SubscriptionsState = DomainState<SubscriptionResponse>;
