import type { SubscriptionPlan } from './SubscriptionPlan'; // if defined separately

export type SubscriptionStatus =
  | 'created'
  | 'authenticated'
  | 'active'
  | 'pending'
  | 'halted'
  | 'cancelled'
  | 'completed'
  | 'expired';

export type Subscription = {
  id: string;
  user: string;
  plan: SubscriptionPlan;
  gateway_subscription_id: string;
  gateway_short_url?: string | null;
  status: SubscriptionStatus;
  charge_at?: string | null;
  start_at?: string | null;
  end_at?: string | null;
  current_start?: string | null;
  current_end?: string | null;
  quantity: number;
  total_count: number;
  remaining_count: number;
  paid_count: number;
  notes: Record<string, any>;
  has_scheduled_changes: boolean;
  change_scheduled_at?: string | null;
  created_at: string;
  updated_at: string;
};

export type TokenUsage = {
  total: number;
  used: number;
  remaining: number;
  expires_at: string;
};
