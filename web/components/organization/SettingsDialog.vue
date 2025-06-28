<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" @close="$emit('close')" class="relative z-20">
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
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-lg bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
              <div class="flex items-center justify-between mb-6">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100">
                  Organization Settings
                </DialogTitle>
                <button
                    class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    @click="$emit('close')"
                >
                  <X class="h-5 w-5 text-gray-500 dark:text-gray-400"/>
                </button>
              </div>

              <form @submit.prevent="handleSubmit" class="space-y-6">
                <!-- Theme Selection -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Theme
                  </label>
                  <div class="grid grid-cols-4 lg:grid-cols-8 gap-3">
                    <button
                        v-for="theme in themes"
                        :key="theme.id"
                        type="button"
                        class="aspect-square rounded-lg border-2 flex items-center justify-center transition-colors"
                        :class="form.theme === theme.id ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'"
                        @click="form.theme = theme.id"
                    >
                      <div class="h-4 w-4 rounded-full" :style="{ backgroundColor: theme.color }"></div>
                    </button>
                  </div>
                </div>

                <!-- Tagline -->
                <div>
                  <label for="tagline" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Tagline
                  </label>
                  <textarea
                      id="tagline"
                      v-model="form.tagline"
                      rows="4"
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      placeholder="A short description of your organization"
                  ></textarea>
                </div>

                <!-- Highlights -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Highlights
                  </label>
                  <div class="space-y-2">
                    <div v-for="(highlight, index) in form.highlights" :key="index" class="flex items-center gap-2">
                      <input
                          v-model="form.highlights[index]"
                          type="text"
                          class="flex-1 rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                          placeholder="Feature highlight"
                      />
                    </div>
                  </div>
                </div>

                <!-- Logo URLs -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label for="logo-light" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Light Logo URL
                    </label>
                    <input
                        id="logo-light"
                        v-model="form.logo_light"
                        type="text"
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                        placeholder="https://example.com/logo-light.svg"
                    />
                  </div>
                  <div>
                    <label for="logo-dark" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Dark Logo URL
                    </label>
                    <input
                        id="logo-dark"
                        v-model="form.logo_dark"
                        type="text"
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                        placeholder="https://example.com/logo-dark.svg"
                    />
                  </div>
                </div>

                <!-- Icon URL -->
                <div>
                  <label for="icon" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Icon URL
                  </label>
                  <input
                      id="icon"
                      v-model="form.icon"
                      type="text"
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      placeholder="https://example.com/icon.svg"
                  />
                </div>

                <!-- Preview -->
                <div>
                  <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Preview</h4>
                  <div class="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                    <div class="flex items-center gap-3 mb-4">
                      <div class="h-10 w-10 rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                        <img v-if="form.icon" :src="form.icon" alt="Icon" class="h-6 w-6"/>
                        <div v-else class="h-6 w-6 bg-gray-300 dark:bg-gray-600 rounded"></div>
                      </div>
                      <div>
                        <div class="h-6 w-32">
                          <img v-if="isDark ? form.logo_dark : form.logo_light" :src="isDark ? form.logo_dark : form.logo_light" alt="Logo" class="h-full"/>
                          <div v-else class="h-full w-full bg-gray-300 dark:bg-gray-600 rounded"></div>
                        </div>
                      </div>
                    </div>
                    <div class="text-sm text-gray-600 dark:text-gray-300 mb-3">{{ form.tagline || 'Your organization tagline' }}</div>
                    <div class="flex flex-wrap gap-2">
                      <div v-for="(highlight, index) in form.highlights" :key="index"
                           class="px-2 py-1 rounded-full text-xs font-medium"
                           :class="getHighlightClass(index)">
                        {{ highlight }}
                      </div>
                    </div>
                  </div>
                </div>

                <div class="flex justify-end gap-3">
                  <button
                      type="button"
                      class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                      @click="$emit('close')"
                  >
                    Cancel
                  </button>
                  <button
                      type="submit"
                      class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                      :disabled="isSubmitting"
                  >
                    {{ isSubmitting ? 'Saving...' : 'Save Changes' }}
                  </button>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {X} from 'lucide-vue-next'
import type {OrganizationConfiguration} from '~/types/organization'

const props = defineProps<{
  show: boolean
  initialConfig?: OrganizationConfiguration
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'update', config: OrganizationConfiguration): void
}>()

const isDark = ref(false)
const isSubmitting = ref(false)

const themes = [
  {id: 'marigold', color: '#f59e0b'},
  {id: 'emerald', color: '#10b981'},
  {id: 'indigo', color: '#6366f1'},
  {id: 'rose', color: '#f43f5e'},
  {id: 'purple', color: '#a855f7'},
  {id: 'cyan', color: '#06b6d4'},
  {id: 'amber', color: '#d97706'},
  {id: 'blue', color: '#3b82f6'}
]

const form = ref({
  theme: 'marigold',
  tagline: '',
  highlights: ['', '', ''],
  logo_light: '',
  logo_dark: '',
  icon: ''
})

onMounted(() => {
  // Check for dark mode
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  isDark.value = savedTheme === 'dark' || (!savedTheme && prefersDark)

  // Initialize form with provided config
  if (props.initialConfig) {
    form.value = {
      theme: props.initialConfig.theme || 'marigold',
      tagline: props.initialConfig.tagline || '',
      highlights: props.initialConfig.highlights || ['', '', ''],
      logo_light: props.initialConfig.logo_light || '',
      logo_dark: props.initialConfig.logo_dark || '',
      icon: props.initialConfig.icon || ''
    }
  }
})

const getHighlightClass = (index: number) => {
  const colors = ['bg-primary-100 text-primary-800 dark:bg-primary-900/50 dark:text-primary-300',
    'bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-300',
    'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300']
  return colors[index % colors.length]
}

const handleSubmit = () => {
  isSubmitting.value = true

  // Filter out empty highlights
  const filteredHighlights = form.value.highlights.filter(h => h.trim() !== '')

  const config = {
    theme: form.value.theme,
    tagline: form.value.tagline,
    highlights: filteredHighlights,
    logo_light: form.value.logo_light,
    logo_dark: form.value.logo_dark,
    icon: form.value.icon
  }

  // Simulate API call
  setTimeout(() => {
    emit('update', config)
    isSubmitting.value = false
  }, 500)
}
</script>