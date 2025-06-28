import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DataSource } from '~/types/data_source'
import { DataSourcesApi } from '~/api/data_sources'

export const useDataSourcesStore = defineStore('dataSources', () => {
  const dataSources = ref<DataSource[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new DataSourcesApi()

  async function getDataSource(id: string) {
    error.value = null

    try {
      const { data, error: apiError } = await api.get(id)
      if (apiError) {
        throw apiError
      }
      return { data, error: null }
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching data source:', e)
      return { data: null, error: e as Error }
    }
  }

  async function fetchDataSources() {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.list()
      if (apiError) {
        throw apiError
      }
      dataSources.value = data || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching data sources:', e)
    } finally {
      loading.value = false
    }
  }

  async function createDataSource(files?: FileList, url?: string | null, conversationId?: string | null, spaceId?: string | null) {
    loading.value = true
    error.value = null

    try {
      const response = await api.create(files, url, conversationId, spaceId)
      return {
        ok: response.ok,
        status: response.status,
        body: response.body
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error creating data source:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteDataSource(id: string) {
    loading.value = true
    error.value = null

    try {
      const { error: apiError } = await api.delete(id)
      if (apiError) {
        throw apiError
      }
      dataSources.value = dataSources.value.filter(ds => ds.id !== id)
    } catch (e) {
      error.value = e as Error
      console.error('Error deleting data source:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    dataSources,
    loading,
    error,

    // Actions
    fetchDataSources,
    createDataSource,
    deleteDataSource,
    getDataSource
  }
})