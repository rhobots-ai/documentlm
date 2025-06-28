import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type {ApiKey} from "~/api/keys";
import {KeysApi} from "~/api/keys";

export const useKeysStore = defineStore('keys', () => {
  const keys = ref<ApiKey[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new KeysApi()

  // Actions
  async function fetchKeys() {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.getKeys()
      if (apiError) {
        throw apiError
      }

      keys.value = data.results || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching keys:', e)
    } finally {
      loading.value = false
    }
  }

  async function createKey(name: string, expiryDays: number) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.createKey({
        name,
        'expiry_days': expiryDays
      })

      if (apiError) {
        throw apiError
      }

      if (data) {
        keys.value.unshift(data)
      }

      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error creating key:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function revokeKey(digest: string) {
    loading.value = true
    error.value = null

    try {
      const { error: apiError } = await api.revokeKey(digest)
      if (apiError) {
        throw apiError
      }

      // Remove the key from the list
      keys.value = keys.value.filter(k => k.digest !== digest)

    } catch (e) {
      error.value = e as Error
      console.error('Error revoking key:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function revokeAll() {
    loading.value = true
    error.value = null

    try {
      const { error: apiError } = await api.revokeAll()
      if (apiError) {
        throw apiError
      }

      // Clear all keys
      keys.value = []

    } catch (e) {
      error.value = e as Error
      console.error('Error revoking all keys:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    keys,
    loading,
    error,
    fetchKeys,
    createKey,
    revokeKey,
    revokeAll
  }
})