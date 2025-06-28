<template>
  <div
      ref="messageContainer"
      :class="[
      'flex items-start gap-2 relative',
      message.role === 'agent' ? 'animate-in fade-in slide-in-from-left-2 group' : 'justify-end animate-in fade-in slide-in-from-right-2 group w-full'
    ]"
  >
    <!-- Selection Indicator -->
    <div
        v-if="isSelected"
        class="absolute -inset-[0.05rem] rounded-lg bg-primary-100/50 dark:bg-primary-900/20 pointer-events-none"
    />

    <!-- Message Content -->
    <div :class="['flex-1', { 'order-1': message.role === 'user' }]">
      <div class="relative">
        <div
            :class="[
          'rounded-lg',
          message.role === 'agent' ? 'p-3' : 'bg-gray-200 dark:bg-gray-800 text-black dark:text-white p-3 w-4/5 ml-auto'
        ]"
        >
          <!-- Thinking Button (only for agent messages with reasoning) -->
          <div v-if="message.role === 'agent' && message.reason_content" class="mb-2">
            <button
                @click.prevent="isThinkingExpanded = !isThinkingExpanded"
                class="flex items-center gap-1.5 px-2 py-1 text-xs font-medium rounded-md bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            >
              <Brain class="h-3 w-3" />
              <span>Thoughts</span>
              <Loader2 v-if="isTyping" class="h-3 w-3 text-primary-500 dark:text-primary-400 animate-spin" />
              <ChevronDown
                  class="h-3 w-3 transition-transform"
                  :class="{ 'rotate-180': isThinkingExpanded }"
              />
            </button>

            <!-- Thinking Content -->
            <div
                v-show="isThinkingExpanded"
                class="mt-2 p-3 text-xs font-mono bg-gray-50 dark:bg-gray-800 rounded-md border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 whitespace-pre-wrap overflow-auto max-h-80"
            >
              <p v-html="md.render(message.reason_content)"/>
            </div>
          </div>

          <p
              :class="{ 'text-gray-900 dark:text-gray-100': message.role === 'agent' }"
              class="text-sm leading-loose prose prose-sm max-w-none prose-p:my-2 prose-p:leading-relaxed prose-headings:mt-4 prose-headings:mb-2 prose-pre:bg-gray-50 dark:prose-pre:bg-gray-800 prose-pre:p-3 prose-pre:rounded-lg prose-code:text-primary-600 dark:prose-code:text-primary-400 prose-code:bg-primary-50 dark:prose-code:bg-primary-900/50 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded-md prose-code:before:content-none prose-code:after:content-none prose-a:text-primary-600 dark:prose-a:text-primary-400 prose-a:no-underline hover:prose-a:underline prose-strong:text-gray-900 dark:prose-strong:text-gray-100 prose-em:text-gray-700 dark:prose-em:text-gray-300"
              v-html="md.render(message.content)"
          />

          <!-- Message Toolbar -->
          <div
              class="absolute w-full -bottom-6 left-0 flex items-center md:opacity-0 md:group-hover:opacity-100 transition-opacity"
              :class="{
                        'right-0 justify-end': message.role === 'user',
                        'justify-between': message.role === 'agent',
                        '-bottom-8': props.isSelected
                    }"
          >
            <div class="flex items-center gap-1">
              <button
                  v-if="message.role === 'agent'"
                  class="p-1 transition-colors text-gray-500 dark:text-gray-400"
                  @click="handleUpvote"
                  :class="{ 'text-primary-600 dark:text-primary-400': message.is_upvote }"
                  title="Upvote"
              >
                <ThumbsUp class="h-3.5 w-3.5 hover:text-primary-600 dark:hover:text-primary-400"/>
              </button>
              <button
                  v-if="message.role === 'agent'"
                  class="p-1 transition-colors text-gray-500 dark:text-gray-400"
                  @click="handleDownvote"
                  :class="{ 'text-red-600 dark:text-red-400': message.is_upvote === false }"
                  title="Downvote"
              >
                <ThumbsDown class="h-3.5 w-3.5 hover:text-red-600 dark:hover:text-red-400"/>
              </button>
              <button
                  class="p-1 transition-colors"
                  @click="copyToClipboard(message.content)"
                  title="Copy message"
              >
                <Copy class="h-3.5 w-3.5 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"/>
              </button>
              <button
                  v-if="message.role === 'agent' && message.mindmap"
                  class="p-1 transition-colors"
                  @click="showMindmap = true"
                  title="View mind map"
              >
                <Network class="h-3.5 w-3.5 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"/>
              </button>
              <button
                  class="p-1 transition-colors"
                  @click="emit('show-add-note', md.render(message.content))"
                  title="Add to Notes"
              >
                <NotebookPen class="h-3.5 w-3.5 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"/>
              </button>
            </div>
            <div class="flex items-center gap-1">
              <button
                  v-if="message.role === 'agent'"
                  class="p-1 transition-colors"
                  @click="$emit('select-message', message, true)"
                  title="Evidences"
              >
                <span
                    class="px-2 py-0.5 rounded-full text-xs font-medium bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400">Evidences</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Mindmap Dialog -->
  <TransitionRoot appear :show="showMindmap" as="template">
    <Dialog as="div" @close="showMindmap = false" class="relative z-10">
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
            <DialogPanel class="w-full transform overflow-hidden rounded-lg bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
              <div class="flex items-center justify-between mb-4">
                <DialogTitle as="h3" class="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Mind Map
                </DialogTitle>
                <button
                    class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    @click="showMindmap = false"
                >
                  <X class="h-5 w-5 text-gray-500 dark:text-gray-400"/>
                </button>
              </div>

              <div class="h-[80vh]">
                <StudioMindMap4 :data="message.mindmap"/>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Brain, ChevronDown, Copy, Loader2, Network, NotebookPen, ThumbsDown, ThumbsUp, X} from 'lucide-vue-next'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import type {Message} from '~/types/message'
import MarkdownIt from 'markdown-it'

const props = defineProps<{
  message: Message
  isSelected?: boolean
  isTyping?: boolean
}>()

const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true,
  langPrefix: 'language-'
})

const emit = defineEmits<{
  (e: 'citation-click'): void
  (e: 'show-add-note', content: string): void
  (e: 'select-message', message: Message, openDeepDive: boolean): void
}>()

const showMindmap = ref(false)
const messageContainer = ref()
const isThinkingExpanded = ref(false)

const messagesStore = useMessagesStore()

const handleUpvote = async () => {
  try {
    await messagesStore.upvoteMessage(props.message.id)
    props.message.is_upvote = true
  } catch (error) {
    console.error('Error upvoting message:', error)
  }
}

const handleDownvote = async () => {
  try {
    await messagesStore.downvoteMessage(props.message.id)
    props.message.is_upvote = false
  } catch (error) {
    console.error('Error downvoting message:', error)
  }
}

const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
  } catch (error) {
    console.error('Failed to copy text:', error)
  }
}

let highlightTimeout = null

const handleMarkClick = (event) => {
  const markLink = event.target.closest('a.mark')
  if (!markLink) return

  event.preventDefault()
  emit('select-message', props.message, true)
  emit('citation-click')

  setTimeout(() => {
    const hash = markLink.getAttribute('href')
    if (!hash.startsWith('#')) return

    // Clear any existing highlight timeout
    if (highlightTimeout) {
      clearTimeout(highlightTimeout)
    }

    // Remove highlight from all mark-* elements
    document.querySelectorAll('[id^="mark-"]').forEach(el => {
      el.classList.remove(
          'bg-yellow-200', 'outline-yellow-400', 'outline'
      )
    })

    const targetId = hash.substring(1) // Remove the #
    const targetElement = document.getElementById(targetId)
    if (!targetElement) return

    // Add your highlight class
    targetElement.classList.add(
        'bg-yellow-200',
        'outline',
        'outline-yellow-400',
        'transition-colors',
        'duration-300'
    )

    // Scroll to the element smoothly
    targetElement.scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    })

    // Set timeout to remove highlight
    highlightTimeout = setTimeout(() => {
      targetElement.classList.remove(
          'bg-yellow-200',
          'outline-yellow-400',
          'outline'
      )
    }, 10000)
  }, 100)
}

onMounted(() => {
  messageContainer.value?.addEventListener('click', handleMarkClick)
})

onUnmounted(() => {
  messageContainer.value?.removeEventListener('click', handleMarkClick)
})
</script>