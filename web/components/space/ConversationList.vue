<template>
  <div>
    <div class="flex items-center justify-between mb-1">
      <div class="flex items-center gap-1">
        <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100">Conversations</h3>
        <span class="px-1 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800 text-sm text-gray-600 dark:text-gray-300">{{ conversations.length }}</span>
      </div>
    </div>

    <!-- Conversation List -->
    <div v-if="conversations.length > 0" class="space-y-3">
      <NuxtLink
        v-for="conversation in conversations"
        :key="conversation.id"
        :to="`/c/${conversation.id}`"
        class="block p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 transition-colors bg-white dark:bg-gray-900 break-words"
      >
        <div class="flex flex-col sm:flex-row items-start justify-between gap-3 sm:gap-4">
          <div class="flex-1 min-w-0">
            <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ conversation.name }}</h4>
            <div class="flex items-center gap-3 mt-2">
              <div class="flex items-center gap-2">
                <div class="h-5 w-5 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                  <User class="h-3 w-3 text-gray-600 dark:text-gray-400" />
                </div>
                <span class="text-xs text-gray-600 dark:text-gray-300">{{ conversation.created_by }}</span>
              </div>
              <span class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(conversation.last_message_at) }}</span>
            </div>
          </div>
          <div class="flex items-center gap-2 mt-2 sm:mt-0">
            <div class="flex items-center gap-1 px-2 py-1 rounded-full bg-gray-50 dark:bg-gray-800 text-xs text-gray-600 dark:text-gray-300">
              <MessageSquare class="h-3 w-3" />
              {{ conversation.message_count }}
            </div>
          </div>
        </div>
      </NuxtLink>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <MessagesSquare class="h-12 w-12 mx-auto text-gray-400 dark:text-gray-600" />
      <h3 class="mt-4 text-lg font-medium text-gray-900 dark:text-gray-100">No conversations yet</h3>
      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Start your first conversation in this space</p>
      <button
          class="mt-4 inline-flex px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
          @click="$emit('startConversation')"
      >
        Start Conversation
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { User, MessageSquare, Files, MessagesSquare } from 'lucide-vue-next'
import type {Conversation} from "~/types/conversation";

defineProps<{
  spaceId: string
  conversations: Conversation[]
}>()

defineEmits<{
  (e: 'startConversation'): void
}>()
</script>