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
              <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/50">
                <Check class="h-6 w-6 text-green-600 dark:text-green-400"/>
              </div>

              <div class="mt-3 text-center">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100">
                  API Key Generated
                </DialogTitle>

                <div class="mt-4">
                  <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
                    Copy your API key now. You won't be able to see it again!
                  </p>

                  <div class="relative">
                    <div class="max-w-full break-all rounded-lg bg-gray-50 dark:bg-gray-800 p-4 font-mono text-sm text-gray-900 dark:text-gray-100">
                      {{ apiKey }}
                    </div>
                    <button
                        class="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
                        @click="copyToClipboard"
                    >
                      <Copy class="h-5 w-5"/>
                    </button>
                  </div>
                </div>
              </div>

              <div class="mt-6">
                <button
                    class="w-full rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
                    @click="$emit('close')"
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
</template>

<script setup lang="ts">
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { Check, Copy } from 'lucide-vue-next'

const props = defineProps<{
  show: boolean
  apiKey: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.apiKey)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>