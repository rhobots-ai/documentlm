import { defineStore } from 'pinia'
import { ref } from 'vue'
import { MessageApi } from '~/api/messages'

export const useMessagesStore = defineStore('messages', () => {
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new MessageApi()

  async function upvoteMessage(id: string) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.upvote(id)
      if (apiError) {
        throw apiError
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error upvoting message:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function downvoteMessage(id: string) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.downvote(id)
      if (apiError) {
        throw apiError
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error downvoting message:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    upvoteMessage,
    downvoteMessage
  }
})