import {defineStore} from 'pinia'
import {computed, ref} from 'vue'
import {SubscriptionPlansApi} from '~/api/subscription_plans'
import type {SubscriptionPlan} from '~/types/subscription_plan'

export const useSubscriptionPlansStore = defineStore('subscriptionPlans', () => {
  const plans = ref<SubscriptionPlan[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new SubscriptionPlansApi()

  // Getters
  const monthlyPlans = computed(() => {
    return plans.value.filter(plan => plan.interval === 'monthly')
  })

  const annualPlans = computed(() => {
    return plans.value.filter(plan => plan.interval === 'yearly')
  })

  // Actions
  async function fetchPlans() {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.list()
      if (apiError) {
        throw apiError
      }
      plans.value = data?.results || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching subscription plans:', e)
    } finally {
      loading.value = false
    }
  }

  async function getPlan(id: string) {
    error.value = null

    try {
      const {data, error: apiError} = await api.get(id)
      if (apiError) {
        throw apiError
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching subscription plan:', e)
      throw e
    }
  }

  return {
    // State
    plans,
    loading,
    error,

    // Getters
    monthlyPlans,
    annualPlans,

    // Actions
    fetchPlans,
    getPlan
  }
})