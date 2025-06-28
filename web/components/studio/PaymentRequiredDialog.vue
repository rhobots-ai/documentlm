<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" @close="$emit('close')" class="relative z-10">
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
              <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-amber-100 dark:bg-amber-900/50">
                <Sparkles class="h-6 w-6 text-amber-600 dark:text-amber-400"/>
              </div>

              <div class="mt-3 text-center">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100">
                  Upgrade to Continue
                </DialogTitle>

                <div class="mt-2">
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    {{ error }}
                  </p>
                  <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                    Upgrade to a higher plan to get more tokens and continue your research journey.
                  </p>
                </div>

                <div class="mt-6 space-y-3">
                  <button
                      class="w-full rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
                      @click="handleUpgrade"
                  >
                    <div class="flex items-center justify-center gap-2">
                      <Sparkles class="h-4 w-4"/>
                      Upgrade Now
                    </div>
                  </button>
                  <button
                      class="w-full rounded-lg border border-gray-200 dark:border-gray-700 px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                      @click="$emit('close')"
                  >
                    Continue with Free Plan
                  </button>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {Sparkles} from 'lucide-vue-next'

const props = defineProps<{
  show: boolean
  error: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const handleUpgrade = () => {
  navigateTo('/my-subscription')
  emit('close')
}
</script>