<template>
  <div class="w-full">
    <div
      class="mx-auto max-w-3xl"
      @dragover.prevent
      @drop.prevent="handleDrop"
    >
      <!-- File Drop Zone -->
      <div
        class="relative rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-primary-500 transition-colors duration-200"
        :class="{ 'border-primary-500 bg-primary-50': isDragging }"
        @dragenter="isDragging = true"
        @dragleave="isDragging = false"
      >
        <div class="flex flex-col items-center">
          <UploadCloud
            class="mx-auto h-12 w-12 text-gray-400"
            :class="{ 'animate-bounce-slow': isDragging }"
          />
          <div class="mt-4">
            <h3 class="text-lg font-medium text-gray-900">
              Drop your document here
            </h3>
            <p class="mt-1 text-sm text-gray-500">
              or click to browse (PDF, DOC, DOCX, TXT)
            </p>
          </div>
          <input
            type="file"
            class="absolute inset-0 h-full w-full cursor-pointer opacity-0"
            accept=".pdf,.doc,.docx,.txt"
            @change="handleFileSelect"
          />
        </div>
      </div>

      <!-- URL Input -->
      <div class="mt-6">
        <div class="flex gap-2">
          <input
            v-model="url"
            type="url"
            placeholder="Or paste a document URL"
            class="input"
          />
          <button
            class="btn-primary whitespace-nowrap"
            :disabled="!url"
            @click="handleUrlSubmit"
          >
            Analyze URL
          </button>
        </div>
      </div>

      <!-- Upload Progress -->
      <TransitionRoot
        as="div"
        :show="isUploading"
        enter="transition-opacity duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity duration-300"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="mt-6">
          <div class="relative pt-1">
            <div class="mb-2 flex items-center justify-between">
              <div>
                <span class="text-xs font-semibold text-primary-600">
                  Uploading...
                </span>
              </div>
              <div class="text-right">
                <span class="text-xs font-semibold text-primary-600">
                  {{ uploadProgress }}%
                </span>
              </div>
            </div>
            <div class="h-2 overflow-hidden rounded bg-gray-200">
              <div
                class="h-2 rounded bg-primary-500 transition-all duration-300"
                :style="{ width: `${uploadProgress}%` }"
              />
            </div>
          </div>
        </div>
      </TransitionRoot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadCloud } from 'lucide-vue-next'
import { TransitionRoot } from '@headlessui/vue'

const emit = defineEmits<{
  (e: 'upload-complete'): void
}>()

const isDragging = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)
const url = ref('')

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
  isUploading.value = true
  uploadProgress.value = 0

  // Simulate upload progress
  const interval = setInterval(() => {
    if (uploadProgress.value < 90) {
      uploadProgress.value += 10
    }
  }, 500)

  try {
    // TODO: Implement actual file upload logic
    await new Promise(resolve => setTimeout(resolve, 3000))
    uploadProgress.value = 100
    setTimeout(() => {
      isUploading.value = false
      uploadProgress.value = 0
      emit('upload-complete')
    }, 500)
  } catch (error) {
    console.error('Upload failed:', error)
  } finally {
    clearInterval(interval)
  }
}

const handleUrlSubmit = async () => {
  if (!url.value) return
  isUploading.value = true
  uploadProgress.value = 0

  try {
    // TODO: Implement URL processing logic
    await new Promise(resolve => setTimeout(resolve, 2000))
    uploadProgress.value = 100
    setTimeout(() => {
      isUploading.value = false
      uploadProgress.value = 0
      emit('upload-complete')
      url.value = ''
    }, 500)
  } catch (error) {
    console.error('URL processing failed:', error)
  }
}
</script>