<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as d3 from 'd3'

const ZOOM_EXTENT = [0.5, 2]

export type MindmapNode = {
  name: string;
  children: MindmapNode[];
};

const props = defineProps<{
  data: MindmapNode
}>()

const svgRef = ref<SVGElement>()

const renderMindmap = () => {
  // Clear existing SVG content
  const existingSvg = d3.select(svgRef.value)
  existingSvg.selectAll('*').remove()

  const width = 1200
  const height = 800
  const dx = 60
  const dy = width / 5
  const margin = { top: 410, right: 120, bottom: 10, left: 240 }
  const buttonWidth = 160
  const buttonHeight = 40
  const buttonPadding = 12
  const controlButtonSize = 40

  // Create zoom behavior
  const zoom = d3.zoom<SVGElement, unknown>()
      .scaleExtent(ZOOM_EXTENT)
      .filter((event) => {
        // Disable mousewheel/scroll zooming
        return !event.type.includes('wheel');
      })
      .on('zoom', (event) => {
        g.attr('transform', event.transform)
      })

  const tree = d3.tree<MindmapNode>()
      .nodeSize([dx, dy])
      .separation((a, b) => 1)

  const root = d3.hierarchy(props.data)
  tree(root)

  const svg = d3.select(svgRef.value)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height])
      .style('user-select', 'none')
      .call(zoom)

  const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top}) scale(1.33)`)

  // Define gradient for node borders
  const gradient = svg.append('defs')
      .append('linearGradient')
      .attr('id', 'borderGradient')
      .attr('x1', '0%')
      .attr('y1', '0%')
      .attr('x2', '100%')
      .attr('y2', '100%')

  gradient.append('stop')
      .attr('offset', '0%')
      .attr('stop-color', '#60a5fa')

  gradient.append('stop')
      .attr('offset', '100%')
      .attr('stop-color', '#a855f7')

  // Define arrow marker
  svg.append('defs').append('marker')
      .attr('id', 'arrowhead')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 28)
      .attr('refY', 0)
      .attr('markerWidth', 8)
      .attr('markerHeight', 8)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#555')

  // Add zoom controls
  const controls = svg.append('g')
      .attr('transform', `translate(${width - 180}, 20)`)

  // Zoom in button
  controls.append('rect')
      .attr('x', 0)
      .attr('y', 0)
      .attr('width', controlButtonSize)
      .attr('height', controlButtonSize)
      .attr('rx', 8)
      .attr('fill', '#ffffff')
      .attr('stroke', '#60a5fa')
      .attr('stroke-width', 2)
      .attr('cursor', 'pointer')
      .on('click', () => {
        svg.transition()
            .duration(300)
            .call(zoom.scaleBy, 1.2)
      })

  controls.append('text')
      .attr('x', controlButtonSize/2)
      .attr('y', controlButtonSize/2 + 6)
      .attr('text-anchor', 'middle')
      .style('font-size', '24px')
      .style('fill', '#60a5fa')
      .style('font-weight', 'bold')
      .style('user-select', 'none')
      .text('+')
      .attr('cursor', 'pointer')
      .on('click', () => {
        svg.transition()
            .duration(300)
            .call(zoom.scaleBy, 1.2)
      })

  // Zoom out button
  controls.append('rect')
      .attr('x', controlButtonSize + 10)
      .attr('y', 0)
      .attr('width', controlButtonSize)
      .attr('height', controlButtonSize)
      .attr('rx', 8)
      .attr('fill', '#ffffff')
      .attr('stroke', '#60a5fa')
      .attr('stroke-width', 2)
      .attr('cursor', 'pointer')
      .on('click', () => {
        svg.transition()
            .duration(300)
            .call(zoom.scaleBy, 0.8)
      })

  controls.append('text')
      .attr('x', controlButtonSize * 1.5 + 10)
      .attr('y', controlButtonSize/2 + 6)
      .attr('text-anchor', 'middle')
      .style('font-size', '24px')
      .style('fill', '#60a5fa')
      .style('font-weight', 'bold')
      .style('user-select', 'none')
      .attr('cursor', 'pointer')
      .text('−')
      .on('click', () => {
        svg.transition()
            .duration(300)
            .call(zoom.scaleBy, 0.8)
      })

  // Fit button
  controls.append('rect')
      .attr('x', controlButtonSize * 2 + 20)
      .attr('y', 0)
      .attr('width', controlButtonSize)
      .attr('height', controlButtonSize)
      .attr('rx', 8)
      .attr('fill', '#ffffff')
      .attr('stroke', '#60a5fa')
      .attr('stroke-width', 2)
      .attr('cursor', 'pointer')
      .on('click', () => {
        fitMap();
      })

  controls.append('text')
      .attr('x', controlButtonSize * 2.5 + 20)
      .attr('y', controlButtonSize/2 + 6)
      .attr('text-anchor', 'middle')
      .style('font-size', '20px')
      .style('fill', '#60a5fa')
      .style('font-weight', 'bold')
      .style('user-select', 'none')
      .text('↺')
      .attr('cursor', 'pointer')
      .on('click', () => {
        fitMap();
      })

  const link = g.append('g')
      .attr('fill', 'none')
      .attr('stroke', '#555')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', 1.5)
      .selectAll('path')
      .data(root.links())
      .join('path')
      .attr('marker-end', 'url(#arrowhead)')
      .attr('d', d => {
        const sourceX = d.source.x;
        const sourceY = d.source.y;
        const targetX = d.target.x;
        const targetY = d.target.y;

        const midY = (sourceY + targetY) / 2;

        return `
        M ${sourceY},${sourceX}
        C ${midY},${sourceX}
          ${midY},${targetX}
          ${targetY},${targetX}
      `;
      })

  const node = g.append('g')
      .attr('stroke-linejoin', 'round')
      .attr('stroke-width', 2)
      .selectAll('g')
      .data(root.descendants())
      .join('g')
      .attr('transform', d => `translate(${d.y},${d.x})`)
      .attr('cursor', 'pointer')
      .on('mouseover', function() {
        d3.select(this).select('rect').attr('fill', '#e2e8f0')
      })
      .on('mouseout', function() {
        d3.select(this).select('rect').attr('fill', '#f8fafc')
      })

  node.append('rect')
      .attr('fill', '#f8fafc')
      .attr('stroke', 'url(#borderGradient)')
      .attr('stroke-width', '2')
      .attr('rx', 6)
      .attr('ry', 6)
      .attr('x', d => d.children ? -buttonWidth - 6 : 6)
      .attr('y', -buttonHeight / 2)
      .attr('width', buttonWidth)
      .attr('height', buttonHeight)

  const textGroups = node.append('g')
      .attr('transform', d => `translate(${d.children ? -buttonWidth - 6 : 6},0)`)

  // Create a foreignObject for HTML-based text rendering
  textGroups.append('foreignObject')
      .attr('x', 0)
      .attr('y', -buttonHeight / 2)
      .attr('width', buttonWidth)
      .attr('height', buttonHeight)
      .append('xhtml:div')
      .style('height', '100%')
      .style('display', 'flex')
      .style('align-items', 'center')
      .style('justify-content', 'center')
      .style('padding', '0 8px')
      .style('color', '#1e293b')
      .style('overflow', 'hidden')
      .style('text-overflow', 'ellipsis')
      .style('white-space', 'nowrap')
      .style('text-wrap', 'auto')
      .style('font-weight', '500')
      .html(d => d.data.name)

  const fitMap = () => {
    const bounds = g.node()?.getBBox()
    if (bounds && bounds.height) {
      const dx = bounds.width;
      const dy = bounds.height;
      const x = bounds.x;
      const y = bounds.y;

      const scale = 0.9 / Math.max(dx / width, dy / height);
      const translate = [width / 2 - scale * (x + dx / 2), height / 2 - scale * (y + dy / 2)];

      svg.transition()
          .duration(500)
          .call(zoom.transform, d3.zoomIdentity
              .translate(translate[0], translate[1])
              .scale(scale));
    }
  }

  // Call fitMap initially to center the mindmap
  fitMap();
}

onMounted(() => {
  renderMindmap()
})

// Watch for changes in the data prop
watch(() => props.data, () => {
  renderMindmap()
})
</script>

<template>
  <svg ref="svgRef"></svg>
</template>

<style scoped>
.mindmap-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

svg {
  max-width: 100%;
  height: auto;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.4;
  background-color: white;
  display: block;
  margin: 0 auto;
}
</style>