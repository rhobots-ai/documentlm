import {defineStore} from 'pinia'
import {ref} from 'vue'
import {TagsApi} from '~/api/tags'
import type {Tag, UpdateTagRequest} from "~/types/tag";

export const useTagsStore = defineStore('tags', () => {
  const tags = ref<Tag[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new TagsApi()

  // Actions
  async function fetchTags() {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.list()
      if (apiError) {
        throw apiError
      }
      tags.value = data['results'] || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching tags:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchTag(id: string) {
    error.value = null

    try {
      const {data, error: apiError} = await api.get(id)
      if (apiError) {
        throw apiError
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching tag:', e)
      throw e
    } finally {
    }
  }

  async function createTag(name: string, color: string, parent_id?: string | null) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.create({
        name,
        color,
        parent_id
      })

      if (apiError) {
        throw apiError
      }

      // Add the new tag to the local state
      if (data) {
        tags.value.push(data);
      }

      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error creating tag:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateTag(id: string, request: UpdateTagRequest) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.update(id, request)

      if (apiError) {
        throw apiError
      }

      // Update the tag in the local state
      if (data) {
        const index = tags.value.findIndex(t => t.id === id);
        if (index !== -1) {
          tags.value[index] = data;
        }
      }

      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error updating tag:', e)
      throw e
    } finally {
      loading.value = false
    }
  }
  async function deleteTag(id: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.delete(id)
      if (apiError) {
        throw apiError
      }

      // Remove the tag from the local state
      tags.value = tags.value.filter(t => t.id !== id);

      return true
    } catch (e) {
      error.value = e as Error
      console.error('Error deleting tag:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    tags,
    loading,
    error,

    // Actions
    fetchTags,
    fetchTag,
    createTag,
    updateTag,
    deleteTag
  }
})