import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ConversationNotesApi } from '~/api/conversation_notes'
import type {ConversationNote} from "~/types/conversation_note";

export const useConversationNotesStore = defineStore('conversationNotes', () => {
  const notes = ref<ConversationNote[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new ConversationNotesApi()

  async function fetchNotes(conversationId: string) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.list({
        conversation: conversationId
      })
      if (apiError) {
        throw apiError
      }
      notes.value = data['results'] || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching notes:', e)
      notes.value = []
    } finally {
      loading.value = false
    }
  }

  async function createNote(conversationId: string, content: string, type: string) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.create({
        conversation: conversationId,
        content,
        type
      })
      if (apiError) {
        throw apiError
      }
      if (data) {
        notes.value.unshift(data)
      }
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error creating note:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateNote(noteId: string, content: string, type: string) {
    loading.value = true
    error.value = null

    try {
      const { data, error: apiError } = await api.update(noteId, {
        content,
        type
      })
      if (apiError) {
        throw apiError
      }

      // Update local state
      const index = notes.value.findIndex(n => n.id === noteId)
      if (index !== -1 && data) {
        notes.value[index] = data
      }
    } catch (e) {
      error.value = e as Error
      console.error('Error updating note:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteNote(noteId: string) {
    loading.value = true
    error.value = null

    try {
      const { error: apiError } = await api.delete(noteId)
      if (apiError) {
        throw apiError
      }
      notes.value = notes.value.filter(n => n.id !== noteId)
    } catch (e) {
      error.value = e as Error
      console.error('Error deleting note:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    notes,
    loading,
    error,

    // Actions
    fetchNotes,
    createNote,
    updateNote,
    deleteNote
  }
})