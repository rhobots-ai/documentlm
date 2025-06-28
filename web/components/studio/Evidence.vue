<template>
  <div class="">
    <div class="flex items-center justify-between mb-3">
      <h3 class="m-0 text-sm font-medium text-gray-700 dark:text-gray-300">Evidences</h3>
    </div>

    <div class="space-y-2 h-full overflow-y-auto text-sm">
      <div
          v-for="(citation, index) in sortedCitations"
          :key="index"
          class="border border-gray-100 dark:border-gray-800 rounded bg-white dark:bg-gray-900"
      >
        <button
            class="w-full px-3 py-2 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            @click="togglePage(index)"
        >
          <div class="flex items-center gap-3 relative group">
            <span class="font-medium text-gray-700 dark:text-gray-300">
              Page {{ citation.page_label }}
              <span
                  class="rounded bg-blue-100 dark:bg-blue-900/50 text-[10px] font-medium text-blue-700 dark:text-blue-400 ring-2 ring-white dark:ring-gray-900 p-1"
                  title="Relevance Score"
              >
              {{ citation.score }}
              </span>
            </span>
            <a
                v-if="citation.data_source_id"
                :href="dataSources.find(ds => ds.id === citation.data_source_id)?.file"
                target="_blank"
                rel="noopener noreferrer"
                class="ml-2"
                @click.stop
                title="Open original document"
            >
              <div class="flex gap-1 justify-items-center text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">
              <ExternalLink class="h-4 w-4 "/>
                <span class="text-sm">Original File</span>
              </div>
            </a>
          </div>
          <ChevronDown
              class="h-4 w-4 text-gray-400 dark:text-gray-500 transition-transform"
              :class="{ 'rotate-180': expandedCitations[index] }"
          />
        </button>
        <div
            v-show="expandedCitations[index]"
            class="px-3 py-2 border-t border-gray-100 dark:border-gray-800 whitespace-pre-wrap font-mono text-xs leading-relaxed"
        >
          <div class="flow-root">
            <button
                v-if="citation.thumbnail"
                class="relative group/preview float-left mr-4 mb-2"
                @click.stop="showPreviewDialog(citation)"
            >
              <img
                  :src="createFullS3URL(citation.thumbnail)"
                  :alt="`Preview of page ${citation.page}`"
                  class="h-40 w-40 object-cover rounded border border-gray-200 dark:border-gray-700 transition-transform group-hover/preview:scale-105"
              />
            </button>
            <div v-html="citation.marked_text" class="text-gray-600 dark:text-gray-400 break-words"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, inject, onMounted, ref} from 'vue'
import {ChevronDown, ExternalLink} from 'lucide-vue-next'
import {createFullS3URL} from "~/utils/url";
import type {Citation} from "~/types/citation";
import type {DataSource} from "~/types/data_source";

const emitter = inject('emitter')
const props = defineProps<{
  citations?: Citation[]
  dataSources: DataSource[]
}>()

onMounted(() => {
  emitter?.on('highlightEvidence', ({pageIndex, chunkIndex}) => {
    expandedCitations.value[pageIndex] = true
    // Scroll the specific chunk into view
    nextTick(() => {
      const chunk = document.querySelector(`[data-page="${pageIndex}"][data-chunk="${chunkIndex}"]`)
      if (chunk) {
        chunk.scrollIntoView({behavior: 'smooth', block: 'center'})
      }
    })
  })
})

const sortedCitations = computed(() => {
  if (!props.citations?.length) {
    return []
  }

  return props.citations.sort((a, b) => b.score - a.score)
})

const expandedCitations = ref<boolean[]>([])

watch(() => props.citations, () => {
  expandedCitations.value = Array(props.citations?.length).fill(true)
}, {immediate: true})

const togglePage = (index: number) => {
  expandedCitations.value[index] = !expandedCitations.value[index]
}

// Preview Dialog
const showPreviewDialog = (citation: Citation) => {
  if (!citation.thumbnail) return

  // Create temporary full-screen dialog
  const dialog = document.createElement('dialog')
  dialog.className = 'fixed z-50 bg-black/75 w-full h-full flex items-center justify-center'

  const container = document.createElement('div')
  container.className = 'relative'

  const img = document.createElement('img')
  img.src = createFullS3URL(citation.thumbnail)
  img.className = 'max-w-[90vw] max-h-[90vh] object-contain'

  const closeButton = document.createElement('button')
  closeButton.className = 'absolute -top-4 -right-4 p-2 rounded-full bg-black backdrop-blur-sm text-white'
  closeButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>'
  closeButton.addEventListener('click', () => dialog.remove())

  container.appendChild(img)
  container.appendChild(closeButton)
  dialog.appendChild(container)

  // Close on click outside or escape
  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) dialog.remove()
  })
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') dialog.remove()
  })

  document.body.appendChild(dialog)
  dialog.showModal()
}

</script>