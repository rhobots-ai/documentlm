<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" class="fixed inset-0 z-50 lg:hidden overflow-hidden" @close="$emit('close')">
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
        <div class="flex min-h-full items-end">
          <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 translate-y-4"
              enter-to="opacity-100 translate-y-0"
              leave="duration-200 ease-in"
              leave-from="opacity-100 translate-y-0"
              leave-to="opacity-0 translate-y-4"
          >
            <DialogPanel class="relative w-full transform bg-white dark:bg-gray-900 p-6 shadow-xl transition-all min-h-[80vh] rounded-t-xl">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">Deep Dive</h2>
                <button
                    class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    @click="$emit('close')"
                >
                  <X class="h-5 w-5 text-gray-500 dark:text-gray-400"/>
                </button>
              </div>
              <StudioDeepDive :message="message" :data-sources="dataSources"/>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import {Dialog, DialogPanel, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {X} from 'lucide-vue-next'
import type {DataSource} from "~/types/data_source";
import type {Message} from "~/types/message";

defineProps<{
  show: boolean
  message?: Message | null
  dataSources: DataSource[]
}>()

defineEmits<{
  (e: 'close'): void
}>()
</script>