<template>
  <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-4 sm:p-6 mb-6">
    <div class="flex flex-col sm:flex-row items-start gap-4 sm:gap-6">
      <div class="h-16 w-16 rounded-xl bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
        <component :is="getSpaceIconComponent(space.icon)" class="h-8 w-8 text-primary-600 dark:text-primary-400"/>
      </div>
      <div class="flex-1">
        <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">{{ space.name }}</h1>
            <div class="mt-1">
              <p class="text-gray-600 dark:text-gray-300">{{ space.description }}</p>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Last updated {{ formatDate(space.updated_at) }}</p>
            </div>
          </div>
          <div class="flex items-center gap-3 sm:flex-shrink-0">
            <button
                v-show="false"
                class="p-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-gray-500 dark:text-gray-400"
                @click="$emit('settings')"
            >
              <Settings class="h-5 w-5"/>
            </button>
            <button
                class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                @click="$emit('startConversation')"
            >
              Talk to Space
            </button>
            <button
                v-show="false"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                :class="space.joined ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400' : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'"
                @click="$emit('update:joined', !space.joined)"
            >
              {{ space.joined ? 'Leave Space' : 'Join Space' }}
            </button>
          </div>
        </div>

        <!-- Space Stats -->
        <div class="flex flex-wrap items-center gap-3 sm:gap-6 mt-4">
          <div v-show="false" class="flex items-center gap-2">
            <Users class="h-5 w-5 text-gray-400 dark:text-gray-500"/>
            <span class="text-sm text-gray-600 dark:text-gray-300">{{ space.members.length }} members</span>
          </div>
          <div class="flex items-center gap-2 cursor-pointer" @click="$emit('show-sources')">
            <Files class="h-5 w-5 text-gray-400 dark:text-gray-500"/>
            <span class="text-sm text-gray-600 dark:text-gray-300">{{ space.data_sources.length }} sources</span>
          </div>
          <div v-show="false" class="flex items-center gap-2">
            <MessageSquare class="h-5 w-5 text-gray-400 dark:text-gray-500"/>
            <span class="text-sm text-gray-600 dark:text-gray-300">{{ space.conversations.length }} conversations</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {Files, MessageSquare, Settings, Users} from 'lucide-vue-next'
import {formatDate} from "~/utils/date";
import type {Space} from "~/types/space";
import {getSpaceIconComponent} from "~/utils/icons";

defineProps<{
  space: Space
}>()

defineEmits<{
  (e: 'startConversation'): void
  (e: 'settings'): void
  (e: 'update:joined', value: boolean): void
  (e: 'show-sources'): void
}>()
</script>