<template>
  <div class="w-full max-w-4xl mx-auto bg-white dark:bg-gray-900 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
    <!-- Input Area -->
    <div class="p-4 bg-white dark:bg-gray-900 rounded-2xl">
      <div class="flex flex-col gap-2">
        <!-- Text Input -->
        <div class="relative">
          <textarea
            v-model="message"
            rows="1"
            class="w-full px-4 py-2 pr-12 rounded-xl border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500 resize-none"
            :class="{ 'h-24': message.split('\n').length > 1 }"
            placeholder="Type your message here or paste a web link"
            @keydown.enter.prevent="handleEnter"
            @input="autoResize"
          ></textarea>

          <!-- Send Button -->
          <button
            class="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full transition-colors"
            :class="message.trim() ? 'text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/50' : 'text-gray-300 dark:text-gray-600'"
            :disabled="!message.trim()"
            @click="sendMessage"
          >
            <SendHorizontal class="h-5 w-5" />
          </button>
        </div>

        <!-- Bottom Controls -->
        <div class="flex items-center gap-2">
        <!-- Web Search Toggle -->
        <button
          class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors relative group"
          :class="{ 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/50 px-3': webSearchEnabled, 'text-gray-500 dark:text-gray-400': !webSearchEnabled }"
          @click="webSearchEnabled = !webSearchEnabled"
        >
          <div class="flex items-center gap-1.5">
            <Globe class="h-5 w-5" />
            <span v-if="webSearchEnabled" class="text-sm font-medium">Web</span>
          </div>
          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
            {{ webSearchEnabled ? 'Disable web search' : 'Enable web search' }}
          </div>
        </button>

        <!-- Attachment Button -->
        <button
          class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors relative group"
          @click="triggerFileInput"
          :class="{ 'text-gray-500 dark:text-gray-400': true }"
        >
          <Paperclip class="h-5 w-5" />
          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
            Attach file
          </div>
        </button>
        <input
          ref="fileInput"
          type="file"
          class="hidden"
          accept=".pdf,.doc,.docx,.txt"
          @change="handleFileAttachment"
        />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Globe, Paperclip, SendHorizontal } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
const message = ref('')
const webSearchEnabled = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileAttachment = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files?.length) {
    router.push('/studio')
  }
}

const autoResize = (event: Event) => {
  const textarea = event.target as HTMLTextAreaElement
  textarea.style.height = 'auto'
  textarea.style.height = textarea.scrollHeight + 'px'
}

const handleEnter = (event: KeyboardEvent) => {
  if (!event.shiftKey) {
    sendMessage()
  }
}

const sendMessage = () => {
  if (!message.value.trim()) return
  
  router.push('/studio')
  message.value = ''
  
  // Reset textarea height
  const textarea = document.querySelector('textarea')
  if (textarea) {
    textarea.style.height = 'auto'
  }
}
</script>