import {defineStore} from 'pinia'
import {computed, ref} from 'vue'
import {SpacesApi} from '~/api/spaces'
import type {Space} from "~/types/space";

export const useSpacesStore = defineStore('spaces', () => {
  const spaces = ref<Space[]>([])
  const currentSpace = ref<Space>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new SpacesApi()

  // Getters
  const joinedSpaces = computed(() => spaces.value.filter(space => space.joined))
  const availableSpaces = computed(() => spaces.value.filter(space => !space.joined))

  // Actions
  async function fetchSpaces() {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.list()
      if (apiError) {
        throw apiError
      }
      spaces.value = data['results'] || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching spaces:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchSpace(id: string) {
    error.value = null

    try {
      const {data, error: apiError} = await api.get(id)
      if (apiError) {
        throw apiError
      }
      currentSpace.value = data
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching space:', e)
      throw e
    } finally {
    }
  }

  async function createSpace(name: string, description: string, icon: string) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.create({
        name,
        description,
        icon
      })

      if (apiError) {
        throw apiError
      }

      if (data) {
        spaces.value.unshift(data)
      }

      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error creating space:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function joinSpace(id: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.join(id)
      if (apiError) {
        throw apiError
      }

      const space = spaces.value.find(s => s.id === id)
      if (space) {
        space.joined = true
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error joining space:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function leaveSpace(id: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.leave(id)
      if (apiError) {
        throw apiError
      }

      const space = spaces.value.find(s => s.id === id)
      if (space) {
        space.joined = false
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error leaving space:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteSpace(id: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.delete(id)
      if (apiError) {
        throw apiError
      }

      spaces.value = spaces.value.filter(s => s.id !== id)
    } catch (e) {
      error.value = e as Error
      console.error('Error deleting space:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    spaces,
    currentSpace,
    loading,
    error,

    // Getters
    joinedSpaces,
    availableSpaces,

    // Actions
    fetchSpaces,
    fetchSpace,
    createSpace,
    joinSpace,
    leaveSpace,
    deleteSpace
  }
})