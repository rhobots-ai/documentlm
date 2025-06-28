<template>
  <div class="mb-6 relative">
    <!-- Loading Overlay -->
    <TransitionRoot
        as="div"
        :show="isLoading"
        enter="transition-opacity duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
        class="absolute inset-0 z-10 flex items-center justify-center bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm rounded-lg"
    >
      <div class="text-center">
        <div class="relative">
          <div class="absolute inset-0 rounded-full bg-primary-100 dark:bg-primary-900/50 animate-ping" style="animation-duration: 2s"/>
          <component
              :is="(uploadStatus ? STATUS_MAP[uploadStatus as keyof typeof STATUS_MAP]?.icon : STATUS_MAP.default.icon)"
              class="relative h-8 w-8 text-primary-600 dark:text-primary-400 mx-auto transition-all duration-300"
              :class="{'animate-pulse': uploadStatus !== 'finished', 'scale-125': uploadStatus === 'finished'}"
          />
        </div>
        <div class="mt-3 flex items-center justify-center gap-2 text-sm font-medium text-gray-900 dark:text-gray-100">
          <span class="transition-all duration-300">{{ uploadStatus ? STATUS_MAP[uploadStatus as keyof typeof STATUS_MAP]?.text : STATUS_MAP.default.text }}</span>
        </div>
      </div>
    </TransitionRoot>

    <!-- File Drop Zone -->
    <div
        class="relative rounded-lg border-2 border-dashed border-gray-300/60 dark:border-gray-600/60 p-8 text-center hover:border-primary-500 dark:hover:border-primary-400 transition-all duration-200 group"
        :class="{ 'border-primary-500 dark:border-primary-400 bg-primary-50/50 dark:bg-primary-900/30': isDragging }"
        @dragenter.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @dragover.prevent
        @drop.prevent="handleDrop"
    >
      <div class="flex flex-col items-center">
        <div class="relative">
          <div class="absolute inset-0 rounded-full bg-primary-100 dark:bg-primary-900/50 animate-ping"
               :class="{ 'opacity-100': isDragging, 'opacity-0 group-hover:opacity-100': !isDragging }" style="animation-duration: 2s"/>
          <UploadCloud
              class="relative mx-auto h-12 w-12 text-primary-500 dark:text-primary-400 transition-transform duration-200 group-hover:scale-110"
              :class="{ 'animate-bounce-slow': isDragging }"
          />
        </div>
        <div class="mt-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">
            Drop your documents here
          </h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            or click to browse (PDF, DOC, DOCX, TXT)
          </p>
        </div>
        <input
            type="file"
            class="absolute inset-0 h-full w-full cursor-pointer opacity-0"
            accept=".pdf,.doc,.docx,.txt"
            multiple
            @change="handleFileSelect"
        />
      </div>
    </div>

    <!-- URL Input -->
    <div class="relative mt-4">
      <div class="flex gap-2">
        <input
            v-model="url"
            type="url"
            placeholder="Or paste a document/web URL"
            class="flex-1 rounded-lg border-gray-300/60 dark:border-gray-600/60 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500 transition-colors"
            :disabled="isLoading"
        />
        <button
            class="px-4 py-2 rounded-lg bg-primary-600/90 backdrop-blur-sm text-white text-sm font-medium hover:bg-primary-700 transition-all disabled:opacity-50 disabled:hover:bg-primary-600/90 hover:shadow-lg hover:shadow-primary-600/20"
            :disabled="!url || isLoading"
            @click="handleUrlSubmit"
        >
          <div class="flex items-center gap-2">
            <Loader2 v-if="isLoading" class="h-4 w-4 animate-spin"/>
            <span>{{ isLoading ? 'Analyzing...' : 'Analyze URL' }}</span>
          </div>
        </button>
      </div>
    </div>

    <!-- Payment Required Dialog -->
    <StudioPaymentRequiredDialog
        :show="showPaymentDialog"
        :error="paymentError"
        @close="showPaymentDialog = false"
    />
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Brain, Loader2, UploadCloud, FileCheck, FileSearch, Save, Database, CheckCircle2} from 'lucide-vue-next'
import {TransitionRoot} from '@headlessui/vue'
import StudioPaymentRequiredDialog from '~/components/studio/PaymentRequiredDialog.vue'
import {useDataSourcesStore} from '~/stores/data_sources'
import type {Conversation} from "~/types/conversation";

const STATUS_MAP = {
  default: {
    text: 'Processing Documents',
    icon: Brain
  },
  files_received: {
    text: 'Files Received',
    icon: FileCheck
  },
  indexing: {
    text: 'Indexing Content',
    icon: Database
  },
  finished: {
    text: 'Processing Complete',
    icon: CheckCircle2
  }
} as const

const props = defineProps<{
  conversationId?: string | null
  spaceId?: string | null
}>()

const emit = defineEmits<{
  (e: 'complete', conversation?: Conversation): void
}>()

const dataSourcesStore = useDataSourcesStore()
const isDragging = ref(false)
const isLoading = ref(false)
const url = ref('')
const showPaymentDialog = ref(false)
const paymentError = ref('')
const uploadStatus = ref(null)

const handleDrop = (e: DragEvent) => {
  isDragging.value = false
  const files = e.dataTransfer?.files
  if (files?.length) {
    handleFiles(files)
  }
}

const handleFileSelect = (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (files?.length) {
    handleFiles(files)
  }
}

const handleFiles = async (files: FileList) => {
  isLoading.value = true
  try {
    const response = await dataSourcesStore.createDataSource(files, null, props.conversationId, props.spaceId)
    if (!response.ok && response.status === 402) {
      showPaymentDialog.value = true
      paymentError.value = response.body?.detail || 'Insufficient tokens'
      return
    }
    emit('complete', response.body.conversation || null)
  } catch (error) {
    console.error('Error uploading file:', error)
  } finally {
    isLoading.value = false
  }
}

const handleUrlSubmit = async () => {
  if (!url.value) return

  isLoading.value = true
  try {
    const response = await dataSourcesStore.createDataSource(null, url.value, props.conversationId, props.spaceId)
    if (!response.ok && response.status === 402) {
      showPaymentDialog.value = true
      paymentError.value = response.body?.detail || 'Insufficient tokens'
      return
    }
    emit('complete', response.body.conversation || null)
  } catch (error) {
    console.error('Error processing URL:', error)
  } finally {
    isLoading.value = false
    url.value = ''
  }
}
</script>