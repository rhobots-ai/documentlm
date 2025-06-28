<template>
  <Dialog as="div" class="relative z-10" @close="$emit('close')" :open="show">
    <div class="fixed inset-0 overflow-y-auto">
      <div class="flex min-h-full items-center justify-center p-4">

        <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-lg bg-white dark:bg-gray-900 p-6 shadow-xl">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
            Rename Conversation
          </h3>

          <form @submit.prevent="handleSubmit">
            <input
                v-model="name"
                type="text"
                class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                placeholder="Enter new name"
                required
            />

            <div class="mt-6 flex justify-end gap-3">
              <button
                  type="button"
                  class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800"
                  @click="$emit('close')"
              >
                Cancel
              </button>
              <button
                  type="submit"
                  class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700"
              >
                Rename
              </button>
            </div>
          </form>
        </DialogPanel>
      </div>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue'
import {Dialog, DialogPanel} from '@headlessui/vue'

const props = defineProps<{
  show: boolean
  initialName: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'rename', name: string): void
}>()

const name = ref(props.initialName)

watch(() => props.initialName, (newName) => {
  name.value = newName
})

const handleSubmit = () => {
  if (!name.value.trim()) return
  emit('rename', name.value)
}
</script>