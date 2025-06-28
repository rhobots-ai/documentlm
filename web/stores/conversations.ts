import {defineStore} from 'pinia'
import {computed, ref} from 'vue'
import type {Conversation} from '~/types/conversation'
import type {CreateConversationRequest} from '~/api/conversations'
import {ConversationsApi} from '~/api/conversations'
import type {ReasoningType} from "~/types/message";

export const useConversationsStore = defineStore('conversations', () => {
  const conversations = ref<Conversation[]>([])
  const nextPage = ref<string | null>(null)
  const hasMore = computed(() => !!nextPage.value)
  const currentConversation = ref<Conversation | null>(null)
  const initialMessage = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new ConversationsApi()

  // Enhanced getters
  const sortedConversations = computed(() => {
    return conversations.value.sort((a, b) => new Date(b.last_message_at).getTime() - new Date(a.last_message_at).getTime())
  })

  async function fetchConversation(id: string) {
    error.value = null

    try {
      const {data, error: apiError} = await api.get(id)
      if (apiError) {
        throw apiError
      }
      currentConversation.value = data
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching conversation:', e)
      throw e
    } finally {
    }
  }

  // Getters
  const spaceConversations = computed(() => (spaceId: string) => {
    return sortedConversations.value.filter(c => c.space === spaceId)
  })

  const personalConversations = computed(() => {
    return sortedConversations.value.filter(c => !c.space)
  })

  // Actions
  async function fetchConversations(reset: boolean = false) {
    loading.value = true
    error.value = null
    const url = reset ? null : nextPage.value

    try {
      const {data, error: apiError} = await api.list(url)
      if (apiError) {
        throw apiError
      }
      if (reset) {
        conversations.value = data.results || []
      } else {
        conversations.value = [...conversations.value, ...(data.results || [])]
      }
      nextPage.value = data.next
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching conversations:', e)
      conversations.value = []
      nextPage.value = null
    } finally {
      loading.value = false
    }
  }

  async function createConversation(request: CreateConversationRequest) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.create(request)
      if (apiError) {
        throw apiError
      }
      if (data) {
        conversations.value.unshift(data)
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error creating conversation:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteConversation(id: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.delete(id)
      if (apiError) {
        throw apiError
      }
      conversations.value = conversations.value.filter(c => c.id !== id)
      if (currentConversation.value.id == id) {
        currentConversation.value = null
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error deleting conversation:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function addDataSource(conversationId: string, dataSourceId: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.addDataSource(conversationId, dataSourceId)
      if (apiError) {
        throw apiError
      }

      // Update local state
      const conversation = conversations.value.find(c => c.id === conversationId)
      if (conversation) {
        conversation.data_sources.push(dataSourceId)
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error adding data source:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function removeDataSource(conversationId: string, dataSourceId: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.removeDataSource(conversationId, dataSourceId)
      if (apiError) {
        throw apiError
      }

      // Update local state
      const conversation = conversations.value.find(c => c.id === conversationId)
      if (conversation) {
        conversation.data_sources = conversation.data_sources.filter(id => id !== dataSourceId)
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error removing data source:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function sendMessage(conversationId: string, message: string, citation: string, reasoning_type: ReasoningType) {
    error.value = null

    try {
      const response = await api.sendMessage(conversationId, message, citation, reasoning_type)
      const {body, error: apiError} = response

      return {
        ok: response.ok,
        status: response.status,
        body
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error sending message:', e)
      throw e
    } finally {
    }
  }

  async function renameConversation(id: string, name: string) {
    error.value = null

    try {
      const {error: apiError} = await api.rename(id, name)
      if (apiError) {
        throw apiError
      }

      // Update local state
      const conversation = conversations.value.find(c => c.id === id)
      if (conversation) {
        conversation.name = name
      }
      if (currentConversation.value.id == id) {
        currentConversation.value.name = name
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error renaming conversation:', e)
      throw e
    } finally {
    }
  }

  return {
    // State
    conversations,
    currentConversation,
    hasMore,
    initialMessage,
    sortedConversations,
    loading,
    error,

    // Getters
    spaceConversations,
    personalConversations,

    // Actions
    fetchConversations,
    createConversation,
    fetchConversation,
    deleteConversation,
    addDataSource,
    removeDataSource,
    sendMessage,
    renameConversation
  }
})