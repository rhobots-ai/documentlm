<template>
  <div class="w-full h-[calc(100vh-36rem)] overflow-hidden">
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
    <div ref="container" class="w-full h-full">
      <!-- D3 will render here -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ZoomIn, ZoomOut, Maximize2 } from 'lucide-vue-next'
import * as d3 from 'd3'

const isDark = ref(false)

onMounted(() => {
  // Check for saved theme preference or system preference
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  isDark.value = savedTheme === 'dark' || (!savedTheme && prefersDark)
})

const container = ref<HTMLElement>()
let svg: d3.Selection<SVGSVGElement, unknown, null, undefined>
let g: d3.Selection<SVGGElement, unknown, null, undefined>
let zoom: d3.ZoomBehavior<Element, unknown>

// Sample mind map data
const data = {
  name: "Document Analysis",
  children: [
    {
      name: "Key Concepts",
      children: [
        { name: "Machine Learning", size: 1 },
        { name: "Neural Networks", size: 1 },
        { name: "Data Processing", size: 1 }
      ]
    },
    {
      name: "Applications",
      children: [
        { name: "Text Analysis", size: 1 },
        { name: "Pattern Recognition", size: 1 }
      ]
    },
    {
      name: "Challenges",
      children: [
        { name: "Data Quality", size: 1 },
        { name: "Processing Speed", size: 1 }
      ]
    }
  ]
}

onMounted(() => {
  if (!container.value) return

  const width = container.value.clientWidth
  const height = container.value.clientHeight

  // Create SVG
  svg = d3.select(container.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)

  // Create main group for zooming
  g = svg.append('g')

  // Create zoom behavior
  zoom = d3.zoom()
    .scaleExtent([0.1, 4])
    .on('zoom', (event) => {
      g.attr('transform', event.transform)
    })

  svg.call(zoom as any)

  // Create hierarchical layout
  const root = d3.hierarchy(data)
  const treeLayout = d3.tree<typeof data>()
    .size([height - 100, width - 200])

  const nodes = treeLayout(root)
  const links = nodes.links()

  // Draw links
  g.selectAll('path')
    .data(links)
    .enter()
    .append('path')
    .attr('d', d3.linkHorizontal()
      .x(d => (d as any).y)
      .y(d => (d as any).x)
    )
    .attr('fill', 'none')
    .attr('stroke', isDark.value ? '#475569' : '#94a3b8')

  // Draw nodes
  const node = g.selectAll('g')
    .data(nodes.descendants())
    .enter()
    .append('g')
    .attr('transform', d => `translate(${d.y},${d.x})`)

  node.append('circle')
    .attr('r', 4)
    .attr('fill', isDark.value ? '#0ea5e9' : '#0284c7')
    .attr('stroke', isDark.value ? '#082f49' : '#e0f2fe')
    .attr('stroke-width', '2')

  node.append('text')
    .attr('dy', '0.31em')
    .attr('x', d => d.children ? -6 : 6)
    .attr('text-anchor', d => d.children ? 'end' : 'start')
    .text(d => d.data.name)
    .attr('fill', isDark.value ? '#f1f5f9' : '#1e293b')
    .attr('font-size', '12px')

  // Center the view
  resetZoom()
})

onUnmounted(() => {
  if (svg) {
    svg.remove()
  }
})

const zoomIn = () => {
  svg.transition().call(zoom.scaleBy as any, 1.5)
}

const zoomOut = () => {
  svg.transition().call(zoom.scaleBy as any, 0.75)
}

const resetZoom = () => {
  const bounds = (g.node() as SVGGElement).getBBox()
  const parent = container.value
  if (!parent) return

  const fullWidth = parent.clientWidth
  const fullHeight = parent.clientHeight
  const width = bounds.width
  const height = bounds.height
  const midX = bounds.x + width / 2
  const midY = bounds.y + height / 2

  const scale = 0.9 / Math.max(width / fullWidth, height / fullHeight)
  const translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY]

  svg.transition()
    .call(
      zoom.transform as any,
      d3.zoomIdentity
        .translate(translate[0], translate[1])
        .scale(scale)
    )
}
</script>