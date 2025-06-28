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
              <div class="flex items-center justify-between mb-6">
                <DialogTitle as="h3" class="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Chat Settings
                </DialogTitle>
                <button
                    class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    @click="$emit('close')"
                >
                  <X class="h-5 w-5 text-gray-500 dark:text-gray-400"/>
                </button>
              </div>

              <div class="space-y-6">
                <!-- Citation Type -->
                <div>
                  <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Citation Type</h4>
                  <div class="space-y-3">
                    <button
                        class="w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-colors"
                        :class="citationType === 'highlight' ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                        @click="citationType = 'highlight'"
                    >
                      <Highlighter class="h-5 w-5" :class="citationType === 'highlight' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'"/>
                      <div class="text-left">
                        <div class="text-sm font-medium"
                             :class="citationType === 'highlight' ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-gray-100'">Highlight
                        </div>
                        <div class="text-xs" :class="citationType === 'highlight' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'">
                          Citations are highlighted in the text
                        </div>
                      </div>
                    </button>

                    <button
                        class="w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-colors"
                        :class="citationType === 'inline' ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                        @click="citationType = 'inline'"
                    >
                      <Link class="h-5 w-5" :class="citationType === 'inline' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'"/>
                      <div class="text-left">
                        <div class="text-sm font-medium"
                             :class="citationType === 'inline' ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-gray-100'">Inline
                        </div>
                        <div class="text-xs" :class="citationType === 'inline' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'">
                          Citations are linked inline with the text
                        </div>
                      </div>
                    </button>
                  </div>
                </div>

                <!-- Reasoning Type -->
                <div>
                  <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Reasoning Type</h4>
                  <div class="space-y-3">
                    <button
                        class="w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-colors"
                        :class="reasoningType === 'simple' ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                        @click="reasoningType = 'simple'"
                    >
                      <Lightbulb class="h-5 w-5" :class="reasoningType === 'simple' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'"/>
                      <div class="text-left">
                        <div class="text-sm font-medium"
                             :class="reasoningType === 'simple' ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-gray-100'">Simple
                        </div>
                        <div class="text-xs" :class="reasoningType === 'simple' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'">
                          Basic reasoning with minimal explanation
                        </div>
                      </div>
                    </button>

                    <button
                        class="w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-colors"
                        :class="reasoningType === 'complex' ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                        @click="reasoningType = 'complex'"
                    >
                      <Brain class="h-5 w-5" :class="reasoningType === 'complex' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'"/>
                      <div class="text-left">
                        <div class="text-sm font-medium"
                             :class="reasoningType === 'complex' ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-gray-100'">Complex
                        </div>
                        <div class="text-xs" :class="reasoningType === 'complex' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'">
                          Detailed step-by-step reasoning
                        </div>
                      </div>
                    </button>

                    <button
                        v-show="false"
                        class="w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-colors"
                        :class="reasoningType === 'react' ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                        @click="reasoningType = 'react'"
                    >
                      <Repeat class="h-5 w-5" :class="reasoningType === 'react' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'"/>
                      <div class="text-left">
                        <div class="text-sm font-medium"
                             :class="reasoningType === 'react' ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-gray-100'">ReAct
                        </div>
                        <div class="text-xs" :class="reasoningType === 'react' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'">
                          Reasoning and acting in iterative steps
                        </div>
                      </div>
                    </button>

                    <button
                        v-show="false"
                        class="w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-colors"
                        :class="reasoningType === 'rewoo' ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                        @click="reasoningType = 'rewoo'"
                    >
                      <Workflow class="h-5 w-5" :class="reasoningType === 'rewoo' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'"/>
                      <div class="text-left">
                        <div class="text-sm font-medium"
                             :class="reasoningType === 'rewoo' ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-gray-100'">ReWOO
                        </div>
                        <div class="text-xs" :class="reasoningType === 'rewoo' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'">
                          Reasoning with out-of-order thinking
                        </div>
                      </div>
                    </button>
                  </div>
                </div>
              </div>

              <div class="mt-6 flex justify-end gap-3">
                <button
                    class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    @click="$emit('close')"
                >
                  Cancel
                </button>
                <button
                    class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                    @click="saveSettings"
                >
                  Save Settings
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
import { ref, watch } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { X, Highlighter, Link, Lightbulb, Brain, Repeat, Workflow } from 'lucide-vue-next'
import type { ReasoningType } from '~/types/message'

const props = defineProps<{
  show: boolean
  initialCitationType: 'highlight' | 'inline'
  initialReasoningType: ReasoningType
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'update', settings: { citationType: 'highlight' | 'inline', reasoningType: ReasoningType }): void
}>()

const citationType = ref<'highlight' | 'inline'>(props.initialCitationType)
const reasoningType = ref<ReasoningType>(props.initialReasoningType)

watch(() => props.initialCitationType, (newValue) => {
  citationType.value = newValue
})

watch(() => props.initialReasoningType, (newValue) => {
  reasoningType.value = newValue
})

const saveSettings = () => {
  emit('update', {
    citationType: citationType.value,
    reasoningType: reasoningType.value
  })
  emit('close')
}
</script>