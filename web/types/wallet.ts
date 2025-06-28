export interface Wallet {
  id: string
  user: string
  organization: string
  balance: string
  currency: string
  created_at: string
  updated_at: string
}

export type WalletTransactionType = 'deposit' | 'api_charge';

export interface WalletTransaction {
  id: string
  wallet: string
  amount: string
  transaction_type: WalletTransactionType
  description: string
  created_at: string
  updated_at: string
}
