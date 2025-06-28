<template>

  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" @close="handleClose" class="relative z-10">
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
            <DialogPanel
                class="w-full max-w-md transform overflow-hidden rounded-lg bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
              <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100 mb-4">
                Document Sources
              </DialogTitle>

              <div class="flex justify-between" v-if="dataSources.length > 50">
                <button
                    class="inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                    @click="handleClose"
                >
                  Close
                </button>
                <button
                    v-if="canAddDataSource"
                    class="inline-flex items-center gap-1.5 justify-center rounded-md border border-transparent bg-primary-600 dark:bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 dark:hover:bg-primary-600"
                    @click="emit('add-data-source')"
                >
                  <Plus class="h-4 w-4"/>
                  Add Source
                </button>
              </div>

              <div class="space-y-3 my-6">
                <template v-if="dataSources.length > 0">
                  <div v-for="source in dataSources" :key="source.id"
                       class="flex items-center justify-between gap-3 p-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
                    <div class="flex items-center gap-2">
                      <div
                          class="h-6 w-6 rounded flex items-center justify-center text-[10px] font-medium"
                          :class="[
                              source.status === 'indexed'
                                ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-400'
                                : source.status === 'errored'
                                  ? 'bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-400'
                                  : 'bg-amber-100 dark:bg-amber-900/50 text-amber-700 dark:text-amber-400'
                            ]"
                      >
                        <template v-if="loadingDataSources[source.id]">
                          <Loader2 class="h-4 w-4 animate-spin"/>
                        </template>
                        <template v-else-if="source.status === 'indexed'">
                          {{ getFileType(source.title) }}
                        </template>
                        <template v-else-if="source.status === 'errored'">
                          !
                        </template>
                        <template v-else>
                          ...
                        </template>
                      </div>
                      <div class="max-w-[240px] truncate text-sm text-gray-900 dark:text-gray-100">{{ source.title }}</div>
                      <a
                          v-if="source.file"
                          :href="source.file"
                          target="_blank"
                          rel="noopener noreferrer"
                          class="ml-2"
                          @click.stop
                          title="Open original document"
                      >
                        <ExternalLink
                            class="h-4 w-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"/>
                      </a>
                    </div>
                    <button class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300">
                      <X class="h-4 w-4"/>
                    </button>
                  </div>
                </template>
                <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
                  <FileQuestion class="h-12 w-12 mx-auto mb-3 text-gray-400 dark:text-gray-600"/>
                  <p class="text-sm">No sources added yet</p>
                  <p class="text-xs mt-1">Add your first document to get started</p>
                </div>
              </div>

              <div class="flex justify-between">
                <button
                    class="inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                    @click="handleClose"
                >
                  Close
                </button>
                <button
                    v-if="canAddDataSource"
                    class="inline-flex items-center gap-1.5 justify-center rounded-md border border-transparent bg-primary-600 dark:bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 dark:hover:bg-primary-600"
                    @click="emit('add-data-source')"
                >
                  <Plus class="h-4 w-4"/>
                  Add Source
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
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from "@headlessui/vue";
import {ExternalLink, FileQuestion, Loader2, Plus, X} from "lucide-vue-next";

import type {DataSource} from '~/types/data_source'
import {ref} from "vue";
import {useDataSourcesStore} from "~/stores/data_sources";

const props = defineProps<{
  show: boolean
  dataSources: DataSource[]
  canAddDataSource: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'add-data-source'): void
}>()

const pollingIntervals = ref<Record<string, NodeJS.Timeout>>({})
const loadingDataSources = ref<Record<string, boolean>>({})

const dataSourcesStore = useDataSourcesStore()

const startPollingDataSource = async (source: DataSource) => {
  if (source.status === 'indexed' || source.status === 'errored') return

  loadingDataSources.value[source.id] = true

  pollingIntervals.value[source.id] = setInterval(async () => {
    try {
      const {data} = await dataSourcesStore.getDataSource(source.id)
      if (data) {
        // Update source status in conversation
        const sourceIndex = props.dataSources.findIndex(s => s.id === source.id)
        if (sourceIndex !== -1) {
          props.dataSources[sourceIndex] = data
        }

        // Stop polling if final status reached
        if (data.status === 'indexed' || data.status === 'errored') {
          clearInterval(pollingIntervals.value[source.id])
          delete pollingIntervals.value[source.id]
          loadingDataSources.value[source.id] = false
        }
      }
    } catch (error) {
      console.error('Error polling data source:', error)
    }
  }, 5000) // Poll every 5 seconds
}

const getFileType = (filename: string) => {
  const ext = filename.split('.').pop()?.toUpperCase() || ''
  return ext.substring(0, 3)
}

const handleClose = () => {
  Object.values(pollingIntervals.value).forEach(interval => clearInterval(interval))
  emit('close')
}

watch(() => props.dataSources, (_) => {
  if (props.dataSources) {
    props.dataSources.filter(ds => ds.status != 'indexed' && ds.status != 'errored').forEach(source => {
      startPollingDataSource(source)
    })
  }
}, {immediate: true})
</script>