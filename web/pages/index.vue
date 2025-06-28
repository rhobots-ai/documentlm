<template>
  <div class="h-[calc(100vh-4rem)] flex items-center justify-center p-6">
    <div class="w-full max-w-2xl mx-auto">
      <!-- Welcome Message -->
      <div class="text-center mb-8">
        <p v-if="isWhiteLabeled" class="mt-6 text-xl md:text-4xl text-gray-600 dark:text-gray-300">{{ whiteLabeledOrganization?.name }}</p>
        <p v-if="isWhiteLabeled" class="mt-6 text-xl text-gray-900 dark:text-gray-400">
          {{ whiteLabeledOrganization?.metadata.tagline }}
        </p>
        <p v-else class="mt-6 text-xl md:text-4xl text-gray-600 dark:text-gray-300">
          Talk to your data, all of it
        </p>
        <div class="mt-6 flex flex-wrap items-center justify-center gap-3">
          <div
              class="flex items-center gap-2 px-2 py-2 rounded-full bg-gradient-to-r from-primary-50 to-purple-50 dark:from-primary-900/30 dark:to-purple-900/30 border border-primary-200/50 dark:border-primary-700/50 text-primary-700 dark:text-primary-300 text-sm font-medium hover:shadow-lg hover:shadow-primary-500/20 dark:hover:shadow-primary-500/10 transition-all duration-300">
            <Sparkles class="h-4 w-4"/>
            <span class="text-xs">{{ highlights[0] }}</span>
          </div>
          <div
              class="flex items-center gap-2 px-2 py-2 rounded-full bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/30 dark:to-teal-900/30 border border-emerald-200/50 dark:border-emerald-700/50 text-emerald-700 dark:text-emerald-300 text-sm font-medium hover:shadow-lg hover:shadow-emerald-500/20 dark:hover:shadow-emerald-500/10 transition-all duration-300">
            <BookOpen class="h-4 w-4"/>
            <span class="text-xs">{{ highlights[1] }}</span>
          </div>
          <div
              class="flex items-center gap-2 px-2 py-2 rounded-full bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/30 dark:to-indigo-900/30 border border-purple-200/50 dark:border-purple-700/50 text-purple-700 dark:text-purple-300 text-sm font-medium hover:shadow-lg hover:shadow-purple-500/20 dark:hover:shadow-purple-500/10 transition-all duration-300">
            <Brain class="h-4 w-4"/>
            <span class="text-xs">{{ highlights[2] }}</span>
          </div>
        </div>
      </div>

      <!-- Quick Space Buttons -->
      <div v-if="spaces.length > 0" class="mb-6">
        <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Your Spaces</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <button
              v-for="space in spaces.slice(0, 4)"
              :key="space.id"
              class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600 bg-white/80 dark:bg-gray-900/80 transition-all hover:shadow-md"
              @click="startConversationInSpace(space.id)"
          >
            <div class="h-10 w-10 rounded-lg bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
              <component :is="getSpaceIconComponent(space.icon)" class="h-5 w-5 text-primary-600 dark:text-primary-400"/>
            </div>
            <div class="text-left">
              <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ space.name }}</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 truncate max-w-[180px]">Have a query? Ask Now</p>
            </div>
          </button>
        </div>
        <div v-if="!isWhiteLabeled" class="mt-3 text-center">
          <NuxtLink
              to="/spaces"
              class="text-sm text-primary-600 dark:text-primary-400 hover:underline"
          >
            View all spaces
          </NuxtLink>
        </div>
      </div>

      <div v-if="isLoggedIn">
        <AddDataSource v-if="!isWhiteLabeled" @complete="handleDataSourceComplete"/>
      </div>

      <AuthLogin v-else/>
    </div>
  </div>
</template>

<script setup lang="ts">
import {BookOpen, Brain, Sparkles} from 'lucide-vue-next'
import type {Conversation} from "~/types/conversation";
import {useOrganizationStore} from "~/stores/organizations";
import {useSpacesStore} from "~/stores/spaces";
import {getSpaceIconComponent} from "~/utils/icons";
import {storeToRefs} from "pinia";

const router = useRouter()
const conversationStore = useConversationsStore()
const organizationStore = useOrganizationStore()
const spacesStore = useSpacesStore()
const {isWhiteLabeled, whiteLabeledOrganization} = storeToRefs(organizationStore)
const {spaces} = storeToRefs(spacesStore)

const userStore = useUserStore()
const {isLoggedIn} = storeToRefs(userStore)

const startConversationInSpace = async (spaceId: string) => {
  // Create conversation in the selected space
  const conversation = await conversationStore.createConversation({
    name: 'New Conversation',
    space_id: spaceId
  })
  // Navigate to the new conversation
  await router.push(`/c/${conversation.id}`)
}

const handleDataSourceComplete = async (conversation?: Conversation) => {
  await conversationStore.fetchConversations(true)
  await router.push({path: `/c/${conversation.id}`})
}

const highlights = computed(() => {
  if (isWhiteLabeled.value) {
    return whiteLabeledOrganization.value?.metadata.highlights
  } else {
    return ['Smart Analysis', 'Citation Support', 'AI Insights']
  }
})

definePageMeta({layout: 'default'})

// Fetch spaces when component mounts
onMounted(() => {
  if(isLoggedIn.value) {
    spacesStore.fetchSpaces()
  }
})
</script>