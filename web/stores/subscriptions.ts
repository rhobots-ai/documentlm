import {defineStore} from 'pinia'
import {ref} from 'vue'
import {SubscriptionsApi} from "~/api/subscriptions";
import type {Subscription, TokenUsage} from "~/types/subscription";

export const useSubscriptionsStore = defineStore('subscriptions', () => {
  const activeSubscription = ref<Subscription>(null)
  const usage = ref<TokenUsage>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new SubscriptionsApi()

  // Actions
  async function getMySubscription() {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.getMySubscription()
      if (apiError) {
        throw apiError
      }
      activeSubscription.value = data || null
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching subscription:', e)
    } finally {
      loading.value = false
    }
  }

  async function getTokenUsage() {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.getTokenUsage()
      if (apiError) {
        throw apiError
      }
      usage.value = data || null
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching usage:', e)
    } finally {
      loading.value = false
    }
  }

  async function createNewSubscription(planId: string) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.create({
        plan_id: planId
      })
      if (apiError) {
        throw apiError
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching subscription:', e)
    } finally {
      loading.value = false
    }
  }

  async function refreshSubscription() {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.refresh()
      if (apiError) {
        throw apiError
      }
      activeSubscription.value = data || null
    } catch (e) {
      error.value = e as Error
      console.error('Error refreshing subscription:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    activeSubscription,
    usage,
    loading,
    error,

    // Actions
    getMySubscription,
    getTokenUsage,
    createNewSubscription,
    refreshSubscription
  }
})