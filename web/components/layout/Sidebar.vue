<template>
  <div
      class="fixed top-0 left-0 h-full w-64 bg-white dark:bg-gray-800 transform transition-transform duration-500 ease-in-out z-20"
      :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
  >
    <div class="flex flex-col h-full overflow-hidden">
      <div class="flex items-center justify-between border-b border-gray-100 dark:border-gray-700">
        <NuxtLink to="/" class="flex items-center">
          <div class="p-3">
            <img
                :src="isWhiteLabeled
                  ? organization.metadata.icon
                  : (isDark ? '/images/icon-dark.svg' : '/images/icon-light.svg')"
                alt="Logo"
                class="h-6"
            />
          </div>
        </NuxtLink>
        <button
            class="p-2 mr-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            @click="$emit('update:isSidebarOpen', false)"
        >
          <PanelLeftClose class="h-5 w-5 text-gray-500 dark:text-gray-400"/>
        </button>
      </div>

      <nav class="flex flex-col h-[calc(100%-10rem)] mt-4">
        <div class="px-4">
          <NuxtLink
              to="/"
              class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
              :class="$route.path === '/' ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
              @click="handleClose"
          >
            <Home v-if="isWhiteLabeled" class="h-5 w-5"/>
            <SquarePen v-else class="h-5 w-5"/>
            {{isWhiteLabeled ? 'Home' : 'Create New'}}
          </NuxtLink>

          <!-- Spaces Link -->
          <NuxtLink
              v-if="isLoggedIn && !isWhiteLabeled"
              to="/spaces"
              class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors mt-1"
              :class="$route.path.startsWith('/spaces') ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
              @click="handleClose"
          >
            <Layout class="h-5 w-5"/>
            Spaces
          </NuxtLink>
        </div>

        <!-- Workspace Navigation -->
        <LayoutWorkspaceNav
            :is-white-labeled="isWhiteLabeled"
            :is-selected="$route.path.startsWith('/workspace')"
            @navigate="handleWorkspaceNavigation"
            @close="handleClose"
        />

        <div class="h-4"/>

        <!-- Scrollable Conversations Section -->
        <div
            ref="scrollContainer"
            class="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent"
            @scroll="handleScroll"
        >
          <!-- All Conversations -->
          <div class="space-y-1">
            <div class="px-3 mb-2">
              <div class="flex items-center justify-between">
                <h4 class="text-xs font-medium text-gray-400 dark:text-gray-500">Conversations</h4>
              </div>
            </div>

            <!-- Loading Skeleton -->
            <div v-if="loading" class="space-y-2">
              <div v-for="n in 3" :key="n" class="px-3 py-2">
                <div class="animate-pulse flex items-center justify-between">
                  <div class="flex-1 space-y-2">
                    <div class="h-4 w-3/4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                    <div class="h-3 w-1/2 bg-gray-200 dark:bg-gray-700 rounded"></div>
                  </div>
                  <div class="h-8 w-8 ml-3 bg-gray-200 dark:bg-gray-700 rounded-full flex-shrink-0"></div>
                </div>
              </div>
            </div>

            <!-- Loading More Indicator -->
            <div v-if="loading && !firstLoad" class="py-4 text-center">
              <div class="inline-flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                <Loader2 class="h-4 w-4 animate-spin"/>
                Loading more...
              </div>
            </div>

            <!-- Conversations List -->
            <div v-else class="px-2">
              <NuxtLink
                  v-for="conversation in sortedConversations"
                  :key="conversation.id"
                  :to="`/c/${conversation.id}`"
                  class="group flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
                  :class="{'bg-gray-200 dark:bg-gray-800': conversationsStore.currentConversation?.id == conversation.id}"
                  @click="handleClose"
                  @click.right.prevent="openMenu($event, conversation)"
              >
                <div class="flex items-center gap-3 flex-1 min-w-0">
                  <div class="relative flex-shrink-0">
                    <div v-if="conversation.unreadCount > 0" class="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-primary-500"></div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="truncate font-medium">{{ conversation.name || 'Untitled Conversation' }}</div>
                    <div class="flex items-center gap-1 text-xs">
                      <span class="text-gray-400 dark:text-gray-500">
                        {{ formatTime(conversation.last_message_at || Date.now()) }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="flex items-center gap-1">
                  <button
                      class="p-1.5 rounded-lg opacity-0 group-hover:opacity-100 hover:bg-gray-100 dark:hover:bg-gray-700 transition-all"
                      @click.stop="openMenu($event, conversation)"
                  >
                    <MoreVertical class="h-4 w-4 text-gray-400 dark:text-gray-500"/>
                  </button>
                  <div
                      v-if="conversation.space"
                      class="h-8 w-8 rounded-full bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center flex-shrink-0"
                      @click.prevent="navigateTo(`/spaces/${conversation.space}`)"
                      title="Go to Space"
                  >
                    <span class="text-xs font-medium text-primary-600 dark:text-primary-400">
                      <Layout class="w-3 h-3"/>
                    </span>
                  </div>
                </div>
              </NuxtLink>
            </div>

            <!-- Context Menu -->
            <div
                v-show="showMenu"
                ref="menu"
                class="fixed z-10 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1"
                :style="{ top: menuPosition.y + 'px', left: menuPosition.x + 'px' }"
            >
              <button
                  class="w-full flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                  @click="handleRename"
              >
                <Pencil class="h-4 w-4"/>
                Rename
              </button>
              <button
                  class="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                  @click="handleDelete"
              >
                <Trash2 class="h-4 w-4"/>
                Delete
              </button>
            </div>

            <!-- Rename Dialog -->
            <StudioRenameDialog
                :show="showRenameDialog"
                :initial-name="selectedConversation?.name || ''"
                @close="showRenameDialog = false"
                @rename="handleRenameSubmit"
            />
          </div>
        </div>

      </nav>

      <div v-if="isLoggedIn" class="p-4 border-t border-gray-100 dark:border-gray-800">
        <LayoutProfileMenu
            :is-dark="isDark"
            :organization="organization"
            :is-white-labeled="isWhiteLabeled"
            @update:is-dark="$emit('update:isDark', $event)"
            @close="handleClose"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import {computed, ref} from 'vue'
  import {useWindowSize} from '@vueuse/core'
  import {Home, Layout, Loader2, MoreVertical, PanelLeftClose, Pencil, SquarePen, Trash2} from 'lucide-vue-next'
  import {storeToRefs} from 'pinia'
  import {useConversationsStore} from '~/stores/conversations'
  import {useUserStore} from '~/stores/user'
  import type {Conversation} from "~/types/conversation";

  const props = defineProps<{
    isSidebarOpen: boolean
    isDark: boolean
    organization?: any
    isWhiteLabeled?: boolean
  }>()

  const conversationsStore = useConversationsStore()
  const userStore = useUserStore()

  const {isLoggedIn} = storeToRefs(userStore)

  const showMenu = ref(false)
  const showRenameDialog = ref(false)
  const menuPosition = ref({x: 0, y: 0})
  const selectedConversation = ref<Conversation | null>(null)
  const menu = ref<HTMLElement | null>(null)

  const openMenu = (event: MouseEvent, conversation: Conversation) => {
    event.preventDefault()
    selectedConversation.value = conversation
    menuPosition.value = {x: event.clientX, y: event.clientY}
    showMenu.value = true

    // Add click outside listener
    nextTick(() => {
      document.addEventListener('click', closeMenu)
    })
  }

  const closeMenu = () => {
    showMenu.value = false
    document.removeEventListener('click', closeMenu)
  }

  const handleRename = () => {
    showMenu.value = false
    showRenameDialog.value = true
  }

  const handleRenameSubmit = async (name: string) => {
    if (!selectedConversation.value) return

    try {
      await conversationsStore.renameConversation(selectedConversation.value.id, name)
      showRenameDialog.value = false
    } catch (error) {
      console.error('Error renaming conversation:', error)
    }
  }

  const handleDelete = async () => {
    if (!selectedConversation.value) return

    if (confirm('Are you sure you want to delete this conversation?')) {
      try {
        await conversationsStore.deleteConversation(selectedConversation.value.id)
        showMenu.value = false
        navigateTo('/')
      } catch (error) {
        console.error('Error deleting conversation:', error)
      }
    }
  }

  onUnmounted(() => {
    document.removeEventListener('click', closeMenu)
  })
  const {sortedConversations, loading, hasMore} = storeToRefs(conversationsStore)
  const scrollContainer = ref<HTMLElement | null>(null)
  const firstLoad = ref(true)
  const scrollPosition = ref(0)

  const handleScroll = () => {
    if (!scrollContainer.value || loading.value || !hasMore.value) return

    const {scrollTop, scrollHeight, clientHeight} = scrollContainer.value
    scrollPosition.value = scrollTop

    // Load more when user scrolls to bottom (with 100 px threshold)
    if (scrollHeight - scrollTop - clientHeight < 100) {
      conversationsStore.fetchConversations().then(() => {
        nextTick(() => {
          if (scrollContainer.value) {
            scrollContainer.value.scrollTop = scrollPosition.value
          }
        })
      })
    }
  }

  watch(() => isLoggedIn.value, (isLoggedInNewValue) => {
    if (isLoggedInNewValue) {
      conversationsStore.fetchConversations(true)
      firstLoad.value = false
    }
  }, {immediate: true})

  const handleWorkspaceNavigation = () => {
    if (isMobile.value) {
      emit('update:isSidebarOpen', false)
    }
  }

  const emit = defineEmits<{
    (e: 'update:isSidebarOpen', value: boolean): void
    (e: 'update:isDark', value: boolean): void
  }>()

  const {width} = useWindowSize()
  const isMobile = computed(() => width.value < 1024)

  const handleClose = () => {
    if (isMobile.value) {
      emit('update:isSidebarOpen', false)
    }
  }

  // Format timestamp
  const formatTime = (timestamp: string | number) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)

    // If a message is from today, show relative time
    if (date.toDateString() === now.toDateString()) {
      if (diffMins < 1) return 'just now'
      if (diffMins === 1) return '1 min ago'
      if (diffMins < 60) return `${diffMins} mins ago`
      if (diffHours === 1) return '1 hour ago'
      return `${diffHours} hours ago`
    }

    // For older messages, show full date and time
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
</script>