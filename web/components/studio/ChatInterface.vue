<template>
  <div
      class="flex flex-col h-full pt-16"
  >
    <div class="flex-1 flex flex-col">
      <!-- Sources Dialog -->
      <TransitionRoot appear :show="showSourcesDialog" as="template">
        <Dialog as="div" @close="showSourcesDialog = false" class="relative z-10">
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
                <DialogPanel
                    class="w-full max-w-md transform overflow-hidden rounded-lg bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100 mb-4">
                    Document Sources
                  </DialogTitle>

                  <div class="space-y-3 mb-6">
                    <template v-if="props.conversation?.data_sources.length > 0">
                      <div v-for="source in props.conversation?.data_sources" :key="source.id"
                           class="flex items-center justify-between gap-3 p-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
                        <div class="flex items-center gap-2">
                          <div
                              class="h-6 w-6 rounded flex items-center justify-center text-[10px] font-medium"
                              :class="[
                                source.status === 'indexed'
                                  ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-400'
                                  : source.status === 'errored'
                                    ? 'bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-400'
                                    : 'bg-amber-100 dark:bg-amber-900/50 text-amber-700 dark:text-amber-400'
                              ]"
                          >
                            <template v-if="loadingDataSources[source.id]">
                              <Loader2 class="h-4 w-4 animate-spin"/>
                            </template>
                            <template v-else-if="source.status === 'indexed'">
                              {{ getFileType(source.title) }}
                            </template>
                            <template v-else-if="source.status === 'errored'">
                              !
                            </template>
                            <template v-else>
                              ...
                            </template>
                          </div>
                          <span class="max-w-[240px] truncate text-sm text-gray-900 dark:text-gray-100">{{ source.title }}</span>
                          <a
                              v-if="source.file"
                              :href="source.file"
                              target="_blank"
                              rel="noopener noreferrer"
                              class="ml-2"
                              @click.stop
                              title="Open original document"
                          >
                            <ExternalLink
                                class="h-4 w-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"/>
                          </a>
                        </div>
                        <button class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300">
                          <X class="h-4 w-4"/>
                        </button>
                      </div>
                    </template>
                    <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
                      <FileQuestion class="h-12 w-12 mx-auto mb-3 text-gray-400 dark:text-gray-600"/>
                      <p class="text-sm">No sources added yet</p>
                      <p class="text-xs mt-1">Add your first document to get started</p>
                    </div>
                  </div>

                  <div class="flex justify-between">
                    <button
                        class="inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                        @click="showSourcesDialog = false"
                    >
                      Close
                    </button>
                    <button
                        class="inline-flex items-center gap-1.5 justify-center rounded-md border border-transparent bg-primary-600 dark:bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 dark:hover:bg-primary-600"
                        @click="handleAddDataSource"
                    >
                      <Plus class="h-4 w-4"/>
                      Add Source
                    </button>
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>

      <!-- Add Source Dialog -->
      <TransitionRoot appear :show="showAddSourcesDialog" as="template">
        <Dialog as="div" @close="showAddSourcesDialog = false" class="relative z-10">
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
                <DialogPanel
                    class="w-full max-w-md transform overflow-hidden rounded-lg bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100 mb-4">
                    Add Data Source
                  </DialogTitle>

                  <AddDataSource @complete="handleDataSourceComplete" :conversation-id="conversation.id"/>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>

      <!-- Chat Messages -->
      <div class="flex-1 flex flex-col justify-center">
        <!-- Empty State -->
        <div v-if="isIndexing" class="text-center py-12">
          <div class="mx-auto w-12 h-12 rounded-full bg-amber-50 dark:bg-amber-900/50 flex items-center justify-center mb-4">
            <Loader2 class="h-6 w-6 text-amber-600 dark:text-amber-400 animate-spin"/>
          </div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Analyzing your data sources</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Please wait while we process and index your data sources
          </p>
        </div>

        <div v-else-if="!messages.length" class="text-center py-12">
          <div class="mx-auto w-12 h-12 rounded-full bg-primary-50 dark:bg-primary-900/50 flex items-center justify-center mb-4">
            <MessageSquare class="h-6 w-6 text-primary-600 dark:text-primary-400"/>
          </div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Start a conversation</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Ask questions about your documents or start a new discussion
          </p>
        </div>

        <div v-else ref="messagesContainer" class="space-y-12 py-4 pb-8">
          <template v-for="(message, index) in messages" :key="index">
            <StudioMessage
                :message="message"
                :is-selected="message === selectedMessage"
                :is-typing="isTyping && message.id === currentMessage?.id"
                @citation-click="handleCitationClick"
                @select-message="handleSelectMessage"
                @show-add-note="handleMessageToNote"
            />
          </template>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="flex items-center gap-2">
            <div class="bg-gray-100 dark:bg-gray-800 rounded-lg rounded-tl-none py-3 px-4">
              <div class="flex gap-1">
                <span class="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce"/>
                <span class="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce [animation-delay:0.2s]"/>
                <span class="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce [animation-delay:0.4s]"/>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Message Input -->
      <div class="sticky bottom-2">
        <!-- Command Suggestions -->
        <div v-show="false" class="py-2 dark:border-gray-800 overflow-x-auto whitespace-nowrap">
          <div class="flex gap-2">
            <button
                v-for="suggestion in suggestions"
                :key="suggestion"
                type="button"
                class="shrink-0 text-sm px-3 py-1.5 rounded-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:border-gray-300 dark:hover:border-gray-600 transition-all"
                @click="newMessage = suggestion"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>

        <form @submit.prevent="sendMessage" class="relative">
          <div class="relative flex items-center">
            <textarea
                v-model="newMessage"
                rows="3"
                @keydown.enter.exact.prevent="sendMessage"
                @keydown.alt.enter.exact.prevent="newMessage += '\n'"
                placeholder="Type a question..."
                class="w-full pr-12 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border border-gray-200/60 dark:border-gray-700/60 focus:ring-0 focus:border-gray-200/60 dark:focus:border-gray-700/60 rounded-t-2xl py-3 px-4 text-gray-900 dark:text-gray-100 placeholder:text-gray-500 dark:placeholder:text-gray-400 resize-none shadow-sm"
            />
            <button
                type="submit"
                class="absolute right-3 p-2 rounded-full bg-primary-600 dark:bg-primary-500 text-white hover:bg-primary-700 dark:hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:hover:bg-primary-600 dark:disabled:hover:bg-primary-500"
                :disabled="!newMessage.trim()"
            >
              <Send class="h-5 w-5"/>
            </button>
          </div>
        </form>

        <!-- Compact Footer -->
        <div
            class="flex items-center justify-between px-4 py-2 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border border-t-0 border-gray-200/60 dark:border-gray-700/60 rounded-b-2xl text-xs">
          <!-- Left Side -->
          <div class="flex items-center gap-1">
            <!-- Space Link -->
            <NuxtLink
                v-if="conversation?.space"
                :to="`/spaces/${conversation.space.id}`"
                target="_blank"
                class="flex items-center gap-1.5 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
            >
              <Layout class="h-4 w-4"/>
              <span class="font-medium">{{ conversation.space.name }}</span>
            </NuxtLink>
            <!-- Sources -->
            <button
                v-else
                class="flex items-center gap-1.5 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
                @click="showSourcesDialog = true"
            >
              <div class="flex -space-x-1">
                <div
                    v-for="source in props.conversation?.data_sources.slice(0, 3)"
                    :key="source.id"
                    class="h-4 w-4 rounded flex items-center justify-center text-[8px] font-medium ring-1 ring-white dark:ring-gray-900"
                    :class="[
                      source.status === 'indexed'
                        ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-400'
                        : source.status === 'errored'
                          ? 'bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-400'
                          : 'bg-amber-100 dark:bg-amber-900/50 text-amber-700 dark:text-amber-400'
                    ]"
                >
                  <template v-if="loadingDataSources[source.id]">
                    <Loader2 class="h-3 w-3 animate-spin"/>
                  </template>
                  <template v-else-if="source.status === 'indexed'">
                    {{ getFileType(source.title) }}
                  </template>
                  <template v-else-if="source.status === 'errored'">
                    !
                  </template>
                  <template v-else>
                    ...
                  </template>
                </div>
              </div>
              <span class="font-medium">{{ props.conversation?.data_sources.length || 0 }} sources</span>
            </button>
            <!-- Settings Button -->
            <div class="flex items-center gap-2">
              <div class="h-4 w-px bg-gray-200 dark:bg-gray-700"/>
              <button
                  class="flex items-center gap-1.5 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
                  @click="showSettingsDialog = true"
              >
                <Settings class="h-4 w-4"/>
                <span class="text-xs">Settings</span>
              </button>
            </div>
          </div>
          <!-- Right Side -->
          <div class="flex items-center gap-1" v-if="!isWhiteLabeled && usage?.remaining < 5000">
            <div class="flex items-center gap-1.5 text-red-600 dark:text-red-400">
              <span class="text-xs">{{ formatNumberCompact(usage?.remaining || 0) }} tokens left</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Selection Popup -->
      <Teleport to="body">
        <div
            ref="selectionPopup"
            class="fixed z-50 opacity-0 pointer-events-none transition-all duration-200 bg-white dark:bg-gray-800 shadow-xl hover:shadow-2xl rounded-lg border border-primary-200 dark:border-primary-700 p-1.5 transform -translate-y-2"
            :class="{ 'opacity-100 pointer-events-auto': isPopupVisible }"
        >
          <button
              @mousedown.prevent
              @click.stop="handleAddToNotes"
              class="flex items-center gap-2 px-3 py-2 text-sm font-medium text-primary-700 dark:text-primary-300 bg-primary-50 dark:bg-primary-900/30 hover:bg-primary-100 dark:hover:bg-primary-900/50 rounded-md transition-colors"
          >
            <Plus class="h-4 w-4"/>
            Add to Notes
          </button>
        </div>
      </Teleport>
    </div>
  </div>

  <!-- Add Note Sidesheet -->
  <StudioAddNoteSidesheet
      v-if="conversation"
      :show="showAddNoteSheet"
      :conversation-id="conversation.id"
      :initial-content="selectedText"
      @close="handleAddNoteClose"
  />

  <!-- Payment Required Dialog -->
  <StudioPaymentRequiredDialog
      :show="showPaymentDialog"
      :error="paymentError"
      @close="showPaymentDialog = false"
  />

  <!-- Alert Dialog -->
  <CommonAlertDialog
      :show="showDialog"
      type="info"
      title="Indexing in progress..."
      message="Please wait while your data sources are being indexed before sending messages."
      button-text="Dismiss"
      @close="showDialog = false"
  />

  <!-- Chat Settings Dialog -->
  <StudioChatSettingsDialog
      :show="showSettingsDialog"
      :initial-citation-type="citationType"
      :initial-reasoning-type="reasoningType"
      @close="showSettingsDialog = false"
      @update="handleSettingsUpdate"
  />
</template>

<script setup lang="ts">
import {computed, ref} from 'vue'
import {ExternalLink, FileQuestion, Layout, Loader2, MessageSquare, Plus, Send, Settings, X} from 'lucide-vue-next'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {formatNumberCompact} from "~/utils/size";
import StudioPaymentRequiredDialog from '~/components/studio/PaymentRequiredDialog.vue'
import type {Conversation} from "~/types/conversation"
import type {Message, ReasoningType} from "~/types/message"
import {useConversationsStore} from '~/stores/conversations';
import {useSubscriptionsStore} from '~/stores/subscriptions';

const subscriptionsStore = useSubscriptionsStore()
const conversationsStore = useConversationsStore()

const {usage} = storeToRefs(subscriptionsStore)
const {initialMessage} = storeToRefs(conversationsStore)

const props = defineProps<{
  conversation: Conversation
  selectedMessage?: Message | null
  isWhiteLabeled?: boolean
}>()

const isIndexing = computed(() => {
  return props.conversation?.data_sources.some(source =>
      source.status !== 'indexed' && source.status !== 'errored'
  )
})

const emitter = defineEmits(['showEvidence', 'updateDeepDive', 'showRenameDialog'])

const messages = computed(() => props.conversation?.messages || [])
const isTyping = ref(false)
const newMessage = ref('')
const showSourcesDialog = ref(false)
const showAddSourcesDialog = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const showPaymentDialog = ref(false)
const paymentError = ref('')
const showDialog = ref(false)
const citationType = ref<'highlight' | 'inline'>('inline')
const reasoningType = ref<ReasoningType>('simple')
const showSettingsDialog = ref(false)

const pollingIntervals = ref<Record<string, NodeJS.Timeout>>({})
const loadingDataSources = ref<Record<string, boolean>>({})

const selectionPopup = ref<HTMLDivElement | null>(null)
const isPopupVisible = ref(false)
const selectedText = ref('')
const showAddNoteSheet = ref(false)

const handleSettingsUpdate = (settings: { citationType: 'highlight' | 'inline', reasoningType: ReasoningType }) => {
  citationType.value = settings.citationType
  reasoningType.value = settings.reasoningType
}


const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      const container = document.getElementById('__nuxt')
      if (container) {
        window.scrollTo(0, container.scrollHeight)
      }
    }
  })
}

// Scroll to bottom when messages load
watch(
    () => props.conversation?.messages,
    () => {
      scrollToBottom()
    },
    {immediate: true}
)

const getFileType = (filename: string) => {
  const ext = filename.split('.').pop()?.toUpperCase() || ''
  return ext.substring(0, 3)
}

// Text selection handling
const handleTextSelection = () => {
  const selection = window.getSelection()
  if (!selection || selection.isCollapsed || !selection.toString().trim()) {
    isPopupVisible.value = false
    return
  }

  const range = selection.getRangeAt(0)
  const rects = range.getClientRects()
  if (rects.length === 0) return

  const popup = selectionPopup.value
  if (!popup) return

  // Ensure popup stays within viewport
  let bottom = 20
  let left = window.innerWidth / 2

  popup.style.bottom = `${bottom}px`
  popup.style.left = `${left}px`
  isPopupVisible.value = true
  popup.style.transform = 'translateY(0)'
  selectedText.value = selection.toString().trim()
}

const handleMouseDown = (e: MouseEvent) => {
  // Hide popup if clicking outside of it
  if (selectionPopup.value && !selectionPopup.value.contains(e.target as Node)) {
    if (selectionPopup.value) {
      selectionPopup.value.style.transform = 'translateY(-8px)'
    }
    isPopupVisible.value = false
  }
}


const handleMouseUp = () => {
  // Use setTimeout to ensure selection is complete
  setTimeout(handleTextSelection, 10)
}

const handleMessageToNote = async (message: any) => {
  selectedText.value = message?.toString().trim() || "";

  await nextTick();
  showAddNoteSheet.value = true;
};


const handleAddToNotes = () => {
  showAddNoteSheet.value = true
  isPopupVisible.value = false

  // Clear selection
  const selection = window.getSelection()
  if (selection) {
    selection.removeAllRanges()
  }
}

const handleAddNoteClose = () => {
  showAddNoteSheet.value = false
  selectedText.value = ''
}

onMounted(async () => {
  document.addEventListener('mouseup', handleMouseUp)
  document.addEventListener('mousedown', handleMouseDown)

  scrollToBottom()

  await subscriptionsStore.getTokenUsage()

  if (initialMessage.value) {
    const message = initialMessage.value
    conversationsStore.initialMessage = null
    newMessage.value = message
    await sendMessage()
  }
})

onUnmounted(() => {
  document.removeEventListener('mouseup', handleMouseUp)
  document.removeEventListener('mousedown', handleMouseDown)

  Object.values(pollingIntervals.value).forEach(interval => clearInterval(interval))
})

const handleAddDataSource = () => {
  showSourcesDialog.value = false
  showAddSourcesDialog.value = true
}

const handleDataSourceComplete = async (conversation?: Conversation) => {
  if (!props.conversation) return

  await conversationsStore.fetchConversation(props.conversation.id)
  showAddSourcesDialog.value = false
}

const suggestions = [
  'Summarize the key points',
  'What are the main findings?',
  'Explain the methodology'
]

const handleCitationClick = () => {
  emitter('showEvidence')
}

const handleSelectMessage = (message: Message, openDeepDive: boolean = false) => {
  emitter('updateDeepDive', message, openDeepDive)
}

let currentMessage: Message | null = null
const sendMessage = async () => {
  if (isIndexing.value) {
    showDialog.value = true
    return
  }

  if (!newMessage.value.trim()) return

  if (!props.conversation) return

  const userMessage = {
    role: 'user' as const,
    content: newMessage.value,
    created_at: new Date().toISOString(),
    conversation_id: props.conversation.id,
    citation_type: citationType.value,
    reasoning_type: reasoningType.value,
    id: crypto.randomUUID()
  }
  if (props.conversation.messages) {
    props.conversation.messages.push(userMessage)
  }
  newMessage.value = ''

  isTyping.value = true
  currentMessage = {
    role: 'agent' as const,
    content: '',
    reason_content: '',
    created_at: new Date().toISOString(),
    conversation_id: props.conversation.id,
    citation_type: citationType.value,
    reasoning_type: reasoningType.value,
    id: crypto.randomUUID()
  }
  let reader = null
  scrollToBottom()
  try {
    const response = await conversationsStore.sendMessage(props.conversation.id, userMessage.content, citationType.value, reasoningType.value)
    if (!response.ok && response.status === 402) {
      const errorData = response.body
      paymentError.value = errorData.detail
      showPaymentDialog.value = true
      return
    }

    const reader = response.body
    if (!reader) {
      throw new Error('No response')
    }

    const decoder = new TextDecoder()

    if (props.conversation.messages) {
      props.conversation.messages.push(currentMessage)
      scrollToBottom()
    }

    while (true) {
      const {done, value} = await reader.read()

      if (done) break

      const chunks = decoder.decode(value).split('\n\n')
      for (const chunk of chunks) {
        if (!chunk) continue

        const [_, event_line, data_line] = chunk.split('\n')
        const event = event_line.replace('event:', '').trim()
        const data = data_line.replace('data:', '').trim()
        let messageIndex = -1
        if (props.conversation.messages) {
          messageIndex = props.conversation.messages.findIndex(m => m.id === currentMessage?.id)
        }
        switch (event) {
          case 'thinking':
            if (messageIndex !== -1) {
              props.conversation.messages[messageIndex].reason_content += JSON.parse(data)
            }
            break

          case 'chunk':
            if (messageIndex !== -1) {
              props.conversation.messages[messageIndex].content += JSON.parse(data)
            }
            break

          case 'final':
            if (messageIndex !== -1) {
              const finalMessage = JSON.parse(data)
              props.conversation.messages[messageIndex].id = finalMessage['id']
              props.conversation.messages[messageIndex].content = finalMessage['content']
              props.conversation.messages[messageIndex].citation = finalMessage['citation']
              props.conversation.messages[messageIndex].citation_type = finalMessage['citation_type']
              props.conversation.messages[messageIndex].mindmap = finalMessage['mindmap']

              if (finalMessage['mindmap'] !== null && (props.conversation.name == null || props.conversation.name.toLowerCase() == 'new conversation')) {
                await conversationsStore.renameConversation(props.conversation.id, finalMessage['mindmap']['name'])
              }

              handleSelectMessage(props.conversation.messages[messageIndex])
              await subscriptionsStore.getTokenUsage()
            }
            break

          case 'complete':
            isTyping.value = false
            break

          case 'error':
            throw new Error(data || 'Unknown error')
        }
      }
    }
  } catch (error) {
    console.error('Error sending message:', error)
  } finally {
    isTyping.value = false
    reader?.cancel()
  }
}
</script>