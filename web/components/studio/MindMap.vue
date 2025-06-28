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
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ZoomIn, ZoomOut, Maximize2 } from 'lucide-vue-next'
import * as d3 from 'd3'
import type { MindmapNode } from '~/types/mindmap'

interface HierarchyNodeWithHidden extends d3.HierarchyNode<MindmapNode> {
  _children?: d3.HierarchyNode<MindmapNode>[];
}

const props = defineProps<{
  data?: MindmapNode | null
}>()

const isDark = ref(document.documentElement.classList.contains('dark'))
const container = ref<HTMLElement>()
let svg: d3.Selection<SVGSVGElement, unknown, null, undefined>
let g: d3.Selection<SVGGElement, unknown, null, undefined>
let zoom: d3.ZoomBehavior<Element, unknown>

// Toggle children visibility
const toggleNode = (d: HierarchyNodeWithHidden) => {
  if (d.children) {
    d._children = d.children
    d.children = undefined
  } else if (d._children) {
    d.children = d._children
    d._children = undefined
  }
  renderMindmap()
}

const renderMindmap = () => {
  if (!container.value || !props.data) return

  const width = container.value.clientWidth
  const height = container.value.clientHeight

  // Clear previous content
  if (svg) {
    svg.selectAll('*').remove()
  } else {
    svg = d3.select(container.value)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
  }

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
  const root = d3.hierarchy(props.data)

  // Initialize all nodes as expanded
  root.descendants().forEach((d: HierarchyNodeWithHidden) => {
    if (d.children) {
      d.children = d.children
      d._children = undefined
    }
  })

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
      .attr('transform', (d: any) => `translate(${d.y},${d.x})`)
      .attr('cursor', d => d.children || d._children ? 'pointer' : 'default')
      .on('click', (event, d: any) => {
        if (d.children || d._children) {
          toggleNode(d)
        }
      })

  // Add button background
  node.append('rect')
      .attr('rx', 6) // Rounded corners
      .attr('ry', 6)
      .attr('x', (d: any) => (d.children || d._children) ? -80 : -60)
      .attr('y', -12)
      .attr('width', (d: any) => (d.children || d._children) ? 160 : 120)
      .attr('height', 24)
      .attr('fill', isDark.value ? '#1e293b' : '#f8fafc')
      .attr('stroke', isDark.value ? '#334155' : '#e2e8f0')
      .attr('stroke-width', 1)
      .attr('class', 'transition-colors duration-200')
      .on('mouseover', function() {
        d3.select(this)
            .attr('fill', isDark.value ? '#334155' : '#f1f5f9')
      })
      .on('mouseout', function() {
        d3.select(this)
            .attr('fill', isDark.value ? '#1e293b' : '#f8fafc')
      })

  node.append('text')
      .attr('dy', '0.31em')
      .attr('x', 0)
      .attr('text-anchor', 'middle')
      .text(d => d.data.name)
      .attr('fill', isDark.value ? '#f1f5f9' : '#1e293b')
      .attr('font-size', '12px')

  // Add expand/collapse indicators
  node.filter((d: any) => d.children || d._children)
      .append('text')
      .attr('dy', '0.31em')
      .attr('x', 65)
      .attr('text-anchor', 'middle')
      .text((d: any) => d.children ? '−' : '+')
      .attr('fill', isDark.value ? '#64748b' : '#94a3b8')
      .attr('font-weight', 'bold')
      .attr('font-size', '12px')

  // Center the view
  resetZoom()
}

onMounted(() => {
  if (props.data) {
    renderMindmap()
  }
})

watch(() => props.data, () => {
  if (props.data) {
    renderMindmap()
  }
}, { deep: true })

watch(() => isDark.value, () => {
  renderMindmap()
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