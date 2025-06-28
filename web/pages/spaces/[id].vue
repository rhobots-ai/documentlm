<template>
  <div class="p-6 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto" v-if="space">
      <SpaceHeader
          :space="space"
          @settings="showSettingsDialog = true"
          @start-conversation="handleStartConversation"
          @show-sources="showDataSourceListDialog = true"
          @update:joined="toggleJoin"
      />

      <!-- Chat Input Card -->
      <div class="my-4 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-0">
        <form @submit.prevent="handleSendMessage" class="relative">
          <textarea
              v-model="message"
              rows="3"
              @keydown.enter.exact.prevent="handleSendMessage"
              @keydown.alt.enter.exact.prevent="message += '\n'"
              placeholder="Interact with this Space"
              class="w-full pr-12 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-0 focus:ring-0 focus:border-gray-200/60 dark:focus:border-gray-700/60 rounded-xl p-4 text-gray-900 dark:text-gray-100 placeholder:text-gray-500 dark:placeholder:text-gray-400 resize-none"
          ></textarea>
          <button
              type="submit"
              class="absolute right-3 bottom-0 -translate-y-1/2 p-2 rounded-full bg-primary-600 dark:bg-primary-500 text-white hover:bg-primary-700 dark:hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:hover:bg-primary-600 dark:disabled:hover:bg-primary-500"
              :disabled="!message.trim()"
          >
            <SendHorizontal class="h-5 w-5"/>
          </button>
        </form>
      </div>

      <ConversationList
          :space-id="space.id"
          :conversations="space.conversations"
          @start-conversation="handleStartConversation"
      />

      <StudioDataSourceListDialog
          :show="showDataSourceListDialog"
          :can-add-data-source="true"
          :data-sources="space.data_sources"
          :space-id="space.id"
          @add-data-source="handleAddDataSource"
          @close="handleDataSourceListClose"/>


      <StudioDataSourceAddDialog
          :show="showDataSourceAddDialog"
          :space-id="space.id"
          @complete="handleDataSourceAddComplete"
          @close="handleDataSourceAddClose"/>


      <!-- Settings Dialog -->
      <TransitionRoot appear :show="showSettingsDialog" as="template">
        <Dialog as="div" @close="showSettingsDialog = false" class="relative z-10">
          <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0"
              enter-to="opacity-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100"
              leave-to="opacity-0"
          >
            <div class="fixed inset-0 bg-black/25"/>
          </TransitionChild>

          <div class="fixed inset-0 overflow-y-auto">
            <div class="flex min-h-full items-center justify-center p-4">
              <TransitionChild
                  as="template"
                  enter="duration-300 ease-out"
                  enter-from="opacity-0 scale-95"
                  enter-to="opacity-100 scale-100"
                  leave="duration-200 ease-in"
                  leave-from="opacity-100 scale-100"
                  leave-to="opacity-0 scale-95"
              >
                <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-lg bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100 mb-6">
                    Space Settings
                  </DialogTitle>

                  <div class="space-y-6">
                    <!-- Visibility -->
                    <div>
                      <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2 sm:mb-3">Visibility</h4>
                      <div class="space-y-3">
                        <button
                            class="w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-colors"
                            :class="!space.isPrivate ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                            @click="space.isPrivate = false"
                        >
                          <Globe class="h-5 w-5" :class="!space.isPrivate ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'"/>
                          <div class="text-left">
                            <div class="text-sm font-medium"
                                 :class="!space.isPrivate ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-gray-100'">Public Space
                            </div>
                            <div class="text-xs" :class="!space.isPrivate ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'">Open
                              for anyone to join and participate
                            </div>
                          </div>
                        </button>

                        <button
                            class="w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-colors"
                            :class="space.isPrivate ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                            @click="space.isPrivate = true"
                        >
                          <Lock class="h-5 w-5" :class="space.isPrivate ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'"/>
                          <div class="text-left">
                            <div class="text-sm font-medium"
                                 :class="space.isPrivate ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-gray-100'">Private Space
                            </div>
                            <div class="text-xs" :class="space.isPrivate ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'">
                              Accessible only to invited users
                            </div>
                          </div>
                        </button>
                      </div>
                    </div>

                    <!-- Unique URL -->
                    <div>
                      <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">Unique URL</h4>
                      <div class="space-y-2 max-w-full">
                        <div v-if="!isEditingUrl" class="flex items-center gap-2">
                          <div class="flex-1 px-3 py-2 bg-gray-50 dark:bg-gray-800 rounded-lg text-sm text-gray-600 dark:text-gray-300 truncate">
                            example.com/spaces/{{ space.uniqueUrl }}
                          </div>
                          <button
                              class="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                              @click="handleUrlEdit"
                          >
                            <Pencil class="h-4 w-4"/>
                          </button>
                        </div>
                        <div v-else class="space-y-2">
                          <div class="flex items-center gap-2">
                            <span class="text-sm text-gray-500 dark:text-gray-400 hidden sm:inline">example.com/spaces/</span>
                            <input
                                v-model="tempUrl"
                                type="text"
                                class="flex-1 rounded-lg border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm"
                                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': urlError }"
                                placeholder="your-space-url"
                            />
                          </div>
                          <div class="flex items-center justify-between">
                            <p v-if="urlError" class="text-xs text-red-500">{{ urlError }}</p>
                            <div class="flex items-center gap-2">
                              <button
                                  class="px-3 py-1.5 rounded-lg text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                                  @click="isEditingUrl = false"
                              >
                                Cancel
                              </button>
                              <button
                                  class="px-3 py-1.5 rounded-lg bg-primary-600 text-white text-sm hover:bg-primary-700 transition-colors"
                                  @click="handleUrlSave"
                              >
                                Save
                              </button>
                            </div>
                          </div>
                        </div>
                        <p class="text-xs text-gray-500 dark:text-gray-400">
                          Choose a unique URL for your space. Only lowercase letters, numbers, and hyphens are allowed.
                        </p>
                      </div>
                    </div>

                    <!-- Share URL -->
                    <div>
                      <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">Share URL</h4>
                      <div class="flex gap-2 max-w-full">
                        <input
                            type="text"
                            :value="space.shareUrl"
                            readonly
                            class="flex-1 bg-gray-50 dark:bg-gray-800 rounded-lg border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100 text-sm truncate"
                        />
                        <div class="relative">
                          <button
                              class="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                              @click="copyToClipboard"
                          >
                            <component :is="copyStatus === 'success' ? Check : Link" class="h-4 w-4"/>
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- Category -->
                    <div>
                      <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">Category</h4>
                      <select
                          v-model="space.category"
                          class="w-full rounded-lg border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm"
                      >
                        <option v-for="category in categories" :key="category.id" :value="category.id">
                          {{ category.name }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <div class="mt-6 flex justify-end">
                    <button
                        class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                        @click="showSettingsDialog = false"
                    >
                      Done
                    </button>
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Check, Globe, Link, Lock, Pencil, SendHorizontal} from 'lucide-vue-next'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import SpaceHeader from '~/components/space/SpaceHeader.vue'
import ConversationList from '~/components/space/ConversationList.vue'

const route = useRoute()
const spacesStore = useSpacesStore()
const conversationsStore = useConversationsStore()
const showSettingsDialog = ref(false)
const copyStatus = ref<'idle' | 'success' | 'error'>('idle')
const message = ref('')
const urlError = ref('')
const isEditingUrl = ref(false)
const tempUrl = ref('')
const showDataSourceListDialog = ref(false)
const showDataSourceAddDialog = ref(false)
const {currentSpace: space} = storeToRefs(spacesStore)
const spaceId = computed(() => route.params.id as string)

watch(() => space.value?.name, (newName) => {
  useHead({
    title: newName || 'Untitled Space'
  })
})

// Fetch space data on mount
onMounted(() => {
  spacesStore.fetchSpace(spaceId.value)
})

// Handle join/leave
const toggleJoin = async () => {
  if (!space.value) return

  try {
    if (space.value.joined) {
      await spacesStore.leaveSpace(space.value.id)
    } else {
      await spacesStore.joinSpace(space.value.id)
    }
    space.value.joined = !space.value.joined
  } catch (error) {
    console.error('Error toggling join status:', error)
  }
}

const handleStartConversation = async () => {
  // create conversation on space
  try {
    const conversation = await conversationsStore.createConversation({
      name: 'New Conversation',
      space_id: spaceId.value
    })
    // navigate to conversation
    navigateTo(`/c/${conversation.id}`)
  } catch (e) {
    if (e.status === 401) {
      navigateTo('/')
    }
  }
}

const handleSendMessage = async () => {
  try {
    if (!message.value.trim() || !space.value) return

    const initialMessage = message.value
    message.value = '' // Clear input early for better UX

    // Store initial message
    conversationsStore.initialMessage = initialMessage

    // Create conversation with initial message
    const conversation = await conversationsStore.createConversation({
      name: initialMessage.slice(0, 50), // Use the first 50 chars as name
      space_id: spaceId.value
    })

    // Navigate to conversation
    await navigateTo(`/c/${conversation.id}`)
  } catch (e) {
    if (e.status === 401) {
      navigateTo('/')
    }
  }
}

const validateUrl = (url: string) => {
  if (!url) return 'URL cannot be empty'
  if (!/^[a-z0-9-]+$/.test(url)) return 'URL can only contain lowercase letters, numbers, and hyphens'
  if (url.length < 3) return 'URL must be at least 3 characters long'
  if (url.length > 50) return 'URL cannot be longer than 50 characters'
  return ''
}

const handleUrlEdit = () => {
  tempUrl.value = space.value.uniqueUrl
  isEditingUrl.value = true
  urlError.value = ''
}

const handleUrlSave = () => {
  const error = validateUrl(tempUrl.value)
  if (error) {
    urlError.value = error
    return
  }

  // TODO: Check if URL is available on the server
  space.value.uniqueUrl = tempUrl.value
  space.value.shareUrl = `https://example.com/spaces/${tempUrl.value}`
  isEditingUrl.value = false
  urlError.value = ''
}

const handleAddDataSource = () => {
  showDataSourceListDialog.value = false
  showDataSourceAddDialog.value = true
}

const handleDataSourceListClose = () => {
  showDataSourceListDialog.value = false
}

const handleDataSourceAddComplete = async () => {
  showDataSourceAddDialog.value = false
  await spacesStore.fetchSpace(spaceId.value)
  showDataSourceListDialog.value = true
}

const handleDataSourceAddClose = () => {
  showDataSourceAddDialog.value = false
}

const copyToClipboard = async () => {
  try {
    if (!navigator?.clipboard) {
      throw new Error('Clipboard API not available')
    }

    await navigator.clipboard.writeText(space.value.shareUrl)
    copyStatus.value = 'success'
    setTimeout(() => {
      copyStatus.value = 'idle'
    }, 2000)
  } catch (error) {
    copyStatus.value = 'error'
    // Fallback: Create a temporary textarea element
    const textarea = document.createElement('textarea')
    textarea.value = space.value.shareUrl
    textarea.style.position = 'fixed'
    textarea.style.opacity = '0'
    document.body.appendChild(textarea)
    textarea.select()

    try {
      document.execCommand('copy')
      copyStatus.value = 'success'
    } catch (err) {
      alert('Press Ctrl+C to copy: ' + space.value.shareUrl)
    } finally {
      document.body.removeChild(textarea)
      setTimeout(() => {
        copyStatus.value = 'idle'
      }, 2000)
    }
  }
}
</script>