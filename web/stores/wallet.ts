import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { WalletApi } from '~/api/wallet'
import type { Wallet, WalletTransaction } from '~/types/wallet'

export const useWalletStore = defineStore('wallet', () => {
  const wallet = ref<Wallet | null>(null)
  const transactions = ref<WalletTransaction[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new WalletApi()

  // Getters
  const balance = computed(() => wallet.value?.balance || 0)
  const currency = computed(() => wallet.value?.currency || 'USD')

  // Actions
  async function fetchWallet() {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.getWallet()
      if (apiError) {
        throw apiError
      }
      wallet.value = data
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching wallet:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchTransactions(walletId: string) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.getTransactions(walletId)
      if (apiError) {
        throw apiError
      }
      transactions.value = data || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching transactions:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    wallet,
    transactions,
    loading,
    error,

    // Getters
    balance,
    currency,

    // Actions
    fetchWallet,
    fetchTransactions
  }
})