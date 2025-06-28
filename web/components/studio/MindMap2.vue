<template>
  <div class="w-full h-[calc(100vh-28rem)] overflow-hidden">
    <div class="flex items-center justify-between p-4 border-b border-gray-200/60 dark:border-gray-700/60">
      <div class="flex gap-2">
        <button
            class="p-1.5 rounded-md bg-white/80 dark:bg-gray-900/80 shadow-sm border border-gray-200/60 dark:border-gray-700/60 hover:bg-white dark:hover:bg-gray-900 hover:border-gray-300 dark:hover:border-gray-600 transition-all"
            @click="zoomIn"
        >
          <ZoomIn class="h-4 w-4 text-gray-600 dark:text-gray-400" />
        </button>
        <button
            class="p-1.5 rounded-md bg-white/80 dark:bg-gray-900/80 shadow-sm border border-gray-200/60 dark:border-gray-700/60 hover:bg-white dark:hover:bg-gray-900 hover:border-gray-300 dark:hover:border-gray-600 transition-all"
            @click="zoomOut"
        >
          <ZoomOut class="h-4 w-4 text-gray-600 dark:text-gray-400" />
        </button>
        <button
            class="p-1.5 rounded-md bg-white/80 dark:bg-gray-900/80 shadow-sm border border-gray-200/60 dark:border-gray-700/60 hover:bg-white dark:hover:bg-gray-900 hover:border-gray-300 dark:hover:border-gray-600 transition-all"
            @click="resetZoom"
        >
          <Maximize2 class="h-4 w-4 text-gray-600 dark:text-gray-400" />
        </button>
      </div>
    </div>
    <div ref="container" class="w-full h-full overflow-auto p-4">
      <div ref="mindmap" class="min-w-full min-h-full"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ZoomIn, ZoomOut, Maximize2 } from 'lucide-vue-next'
import mermaid from 'mermaid'
import type { MindmapNode } from '~/types/mindmap'

const props = defineProps<{
  data?: MindmapNode | null
}>()

const container = ref<HTMLElement>()
const mindmap = ref<HTMLElement>()
let zoom = 1

// Initialize mermaid
onMounted(() => {
  mermaid.initialize({
    startOnLoad: false,
    theme: 'forest',
    mindmap: {
      padding: 16,
      useMaxWidth: false
    }
  })
})

// Generate mindmap diagram definition
const generateMindmapDefinition = (node: MindmapNode, level = 0): string => {
  const indent = '  '.repeat(level)
  let definition = level === 0 ? 'mindmap\n' : ''

  definition += `${indent} ${node.name}\n`

  if (node.children) {
    node.children.forEach(child => {
      definition += generateMindmapDefinition(child, level + 1)
    })
  }
  return definition
}

// Render mindmap
const renderMindmap = async () => {
  if (!mindmap.value || !props.data) return

  const definition = generateMindmapDefinition(props.data)

  try {
    const { svg } = await mermaid.render('mindmap', definition)
    mindmap.value.innerHTML = svg
  } catch (error) {
    console.error('Error rendering mindmap:', error)
  }
}

// Watch for data changes
watch(() => props.data, () => {
  renderMindmap()
}, { deep: true })

// Zoom controls
const zoomIn = () => {
  zoom = Math.min(zoom * 1.2, 3)
  if (mindmap.value) {
    mindmap.value.style.transform = `scale(${zoom})`
  }
}

const zoomOut = () => {
  zoom = Math.max(zoom / 1.2, 0.3)
  if (mindmap.value) {
    mindmap.value.style.transform = `scale(${zoom})`
  }
}

const resetZoom = () => {
  zoom = 1
  if (mindmap.value) {
    mindmap.value.style.transform = `scale(${zoom})`
  }
}

// Initial render
onMounted(() => {
  renderMindmap()
})
</script>