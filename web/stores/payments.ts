import { defineStore } from 'pinia'
import { ref } from 'vue'
import { PaymentsApi } from '~/api/payments'

export const usePaymentsStore = defineStore('payments', () => {
  const payments = ref([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new PaymentsApi()

  async function createPayment(amount: number) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.create({ amount })
      if (apiError) {
        throw apiError
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error creating payment:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updatePaymentStatus(orderId: string, paymentId: string, signature: string) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.updateStatus({
        order_id: orderId,
        payment_id: paymentId,
        signature
      })
      if (apiError) {
        throw apiError
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error updating payment status:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchPayments() {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.list()
      if (apiError) {
        throw apiError
      }
      payments.value = data || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching payments:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    payments,
    loading,
    error,

    // Actions
    createPayment,
    updatePaymentStatus,
    fetchPayments
  }
})