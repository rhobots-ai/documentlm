<template>
  <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow">
    <div class="p-4">
      <!-- Space Header -->
      <NuxtLink :to="{ path: `/spaces/${space.id}` }" class="block">
        <div class="flex items-start justify-between mb-3">
          <div class="flex items-center justify-center gap-3">
            <div class="h-10 w-10 rounded-lg bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
              <component :is="getSpaceIconComponent(space.icon)" class="h-5 w-5 text-primary-600 dark:text-primary-400"/>
            </div>
            <h3 class="m-0 font-medium text-gray-900 dark:text-gray-100">{{ space.name }}</h3>
          </div>
          <button
              v-show="false"
              class="px-3 py-1.5 rounded-full text-xs font-medium transition-colors"
              :class="space.joined ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400' : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'"
              @click.stop="toggleJoin"
          >
            {{ space.joined ? 'Joined' : 'Join' }}
          </button>
        </div>

        <!-- Space Description -->
        <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">{{ space.description }}</p>
      </NuxtLink>

      <!-- Space Stats -->
      <div class="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
        <div class="flex items-center gap-1 cursor-pointer" @click="showDataSourceListDialog = true">
          <Files class="h-4 w-4"/>
          {{ space.data_sources.length }} documents
        </div>
        <div class="flex items-center gap-1 cursor-pointer" @click="navigateTo(`spaces/${space.id}`)">
          <MessageSquare class="h-4 w-4"/>
          {{ space.conversations.length }} conversations
        </div>
      </div>
      <div class="flex w-full mt-3">
        <button
            class="px-3 py-2 w-full rounded-full bg-primary-100 dark:bg-primary-600/50 text-primary-700 dark:text-primary-100 text-sm font-medium transition-colors"
            @click.stop="handleStartConversation"
        >
          Talk to Space
        </button>
      </div>
    </div>

    <StudioDataSourceListDialog
        :show="showDataSourceListDialog"
        :can-add-data-source="false"
        :data-sources="space.data_sources"
        :space-id="space.id"
        @close="handleDataSourceListClose"/>
  </div>
</template>

<script setup lang="ts">
import type {Space} from "~/types/space";
import {Files, MessageSquare} from 'lucide-vue-next'
import {getSpaceIconComponent} from "~/utils/icons";

const props = defineProps<{
  space: Space
}>()
const emit = defineEmits(['update:joined'])

const conversationsStore = useConversationsStore()
const showDataSourceListDialog = ref<boolean>(false)

const toggleJoin = () => {
  emit('update:joined', !props.space.joined)
}

const handleStartConversation = async () => {
  // create conversation on space
  try {
    const conversation = await conversationsStore.createConversation({
      name: 'New Conversation',
      space_id: props.space.id
    })
    // navigate to conversation
    navigateTo(`/c/${conversation?.id}`)
  } catch (e) {
    if (e.status === 401) {
      navigateTo('/')
    }
  }
}

const handleDataSourceListClose = () => {
  showDataSourceListDialog.value = false
}
</script>