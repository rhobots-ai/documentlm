<template>
  <div class="w-full">
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <!-- Summary Header -->
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-semibold text-gray-900">Document Summary</h2>
        <button
          class="text-gray-500 hover:text-gray-700"
          @click="isExpanded = !isExpanded"
        >
          <ChevronDown
            v-if="!isExpanded"
            class="h-5 w-5 transition-transform"
          />
          <ChevronUp
            v-else
            class="h-5 w-5 transition-transform"
          />
        </button>
      </div>

      <!-- Key Metrics -->
      <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="bg-gray-50 rounded-lg p-4">
          <div class="text-sm text-gray-500">Word Count</div>
          <div class="text-2xl font-semibold text-gray-900">2,547</div>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <div class="text-sm text-gray-500">Reading Time</div>
          <div class="text-2xl font-semibold text-gray-900">12 min</div>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <div class="text-sm text-gray-500">Key Points</div>
          <div class="text-2xl font-semibold text-gray-900">8</div>
        </div>
      </div>

      <!-- Detailed Content -->
      <TransitionRoot
        as="div"
        :show="isExpanded"
        enter="transition-all duration-300 ease-out"
        enter-from="transform opacity-0 -translate-y-4"
        enter-to="transform opacity-100 translate-y-0"
        leave="transition-all duration-200 ease-in"
        leave-from="transform opacity-100 translate-y-0"
        leave-to="transform opacity-0 -translate-y-4"
      >
        <div class="space-y-4">
          <div class="border-t border-gray-200 pt-4">
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              Main Topics
            </h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="topic in topics"
                :key="topic"
                class="px-3 py-1 rounded-full bg-primary-100 text-primary-800 text-sm"
              >
                {{ topic }}
              </span>
            </div>
          </div>

          <div class="border-t border-gray-200 pt-4">
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              Key Takeaways
            </h3>
            <ul class="space-y-2 text-gray-600">
              <li
                v-for="(point, index) in keyPoints"
                :key="index"
                class="flex items-start gap-2"
              >
                <div class="mt-1 h-2 w-2 rounded-full bg-primary-500 shrink-0" />
                {{ point }}
              </li>
            </ul>
          </div>
        </div>
      </TransitionRoot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ChevronDown, ChevronUp } from 'lucide-vue-next'
import { TransitionRoot } from '@headlessui/vue'

const isExpanded = ref(false)

// Sample data
const topics = [
  'Machine Learning',
  'Data Analysis',
  'Neural Networks',
  'AI Ethics',
  'Future Trends'
]

const keyPoints = [
  'AI systems continue to evolve at an unprecedented rate',
  'Ethical considerations are becoming increasingly important',
  'Data privacy remains a critical concern',
  'Integration with existing systems poses challenges'
]
</script>