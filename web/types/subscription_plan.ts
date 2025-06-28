export type SubscriptionPlan = {
  id: string;
  name: string;
  gateway: string;
  description: string;
  amount: number;
  currency: string;
  interval: 'daily' | 'weekly' | 'monthly' | 'yearly';
  gateway_plan_id: string;
  tokens: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};
