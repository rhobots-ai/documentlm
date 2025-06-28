<template>
  <div class="w-full h-full overflow-hidden">
    <div ref="toolbarRef" class="absolute right-4 z-10"></div>
    <svg ref="svgRef" class="w-full h-full dark:bg-gray-800"></svg>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref, watch} from 'vue'
import {Transformer} from 'markmap-lib'
import {deriveOptions, Markmap} from 'markmap-view'
import {type IToolbarItem, Toolbar} from 'markmap-toolbar'
import type {MindmapNode} from '~/types/mindmap'
import type {VNode} from "@gera2ld/jsx-dom";

const props = defineProps<{
  data?: MindmapNode | null
}>()

const svgRef = ref<SVGElement>()
const toolbarRef = ref<HTMLElement>()
let markmap: Markmap
let toolbar: Toolbar
const transformer = new Transformer()

const handleExport = async (type: string = 'svg') => {
  if (!svgRef.value) return;

  await markmap.fit()

  const svgEl = svgRef.value;
  const serializer = new XMLSerializer();
  const svgString = serializer.serializeToString(svgEl);

  if (type === 'svg') {
    const blob = new Blob([svgString], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'mindmap.svg';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } else if (type === 'png') {
    const img = new Image();
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgString)));
    img.onload = () => {
      const scale = 10;
      const originWidth = svgEl.width.baseVal.value || 800;
      const originHeight = svgEl.height.baseVal.value || 400;
      const canvas = document.createElement('canvas');
      canvas.width = originWidth * scale;
      canvas.height = originHeight * scale;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.setTransform(scale, 0, 0, scale, 0, 0);
        ctx.drawImage(img, 0, 0,  canvas.width, canvas.height);
        canvas.toBlob((blob) => {
          if (blob) {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'mindmap.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
          }
        }, 'image/png');
      }
    };
  }
};

const customToolbarItems: IToolbarItem[] = [
  {
    id: 'export',
    title: 'Export as PNG',
    onClick: () => {
      handleExport('png')
    },
    content: {
      vtype: 1,
      type: 'svg',
      props: {
        fill: 'none',
        stroke: 'currentColor',
        width: 18,
        height: 18,
        viewBox: '0 0 20 24',
        style: 'padding: 2px',
        'stroke-width': '3',
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        class: 'lucide lucide-download-icon lucide-download',
        innerHTML: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>'
      }
    } as VNode
  }
]

const generateMarkdown = (node: MindmapNode, level = 0): string => {
  const indent = '  '.repeat(level)
  let md = `${indent}- ${node.name}\n`

  if (node.children?.length) {
    node.children.forEach(child => {
      md += generateMarkdown(child, level + 1)
    })
  }

  return md
}

const renderMindmap = () => {
  if (!svgRef.value || !props.data) return

  // Clear existing SVG content
  if (svgRef.value) {
    while (svgRef.value.firstChild) {
      svgRef.value.removeChild(svgRef.value.firstChild)
    }
  }

  markmap = createMindmap(svgRef.value)

  // Delay the fit to ensure proper centering
  setTimeout(() => {
    markmap.fit()
  }, 100)
}

onMounted(() => {
  if (props.data) {
    renderMindmap()

    // Add window resize handler
    window.addEventListener('resize', () => {
      if (markmap) {
        setTimeout(() => {
          markmap.fit()
        }, 100)
      }
    })
  }
})

const createMindmap = (svgElement) => {
  // Convert mindmap data to Markdown format
  const markdown = generateMarkdown(props.data)

  // Transform markdown to markmap data
  const {root} = transformer.transform(markdown)

  // Initialize markmap if not already done
  const tempMarkmap = Markmap.create(svgElement, deriveOptions({
    color: ['#4f47e6'],
    autoFit: true,
    paddingX: 40,
    paddingY: 50,
    duration: 500,
    lineWidth: 2,
    nodeMinHeight: 28,
    spacingVertical: 24,
    spacingHorizontal: 120,
    maxWidth: 200
  }))

  // Initialize toolbar
  if (toolbarRef.value && !toolbar) {
    toolbar = new Toolbar()
    toolbar.setBrand(false)
    toolbar.setItems([...toolbar.items, ...customToolbarItems])
    toolbar.attach(tempMarkmap)
    toolbarRef.value.appendChild(toolbar.el)
  }

  // Render the mindmap
  tempMarkmap.setData(root)

  return tempMarkmap
}

// Clean up resize listener
onUnmounted(() => {
  window.removeEventListener('resize', () => {
    if (markmap) {
      markmap.fit()
    }
  })
})

// Watch for data changes
watch(() => props.data, () => {
  if (props.data) {
    renderMindmap()
  }
}, {deep: true})
</script>

<style>
/* Markmap styles */
.markmap-node {
  cursor: pointer;
  transition: all 0.2s ease;
}

.markmap-node:hover {
  filter: brightness(1.1);
}

.markmap-link {
  transition: all 0.2s ease;
}

.markmap-link:hover {
  stroke-width: 2px;
}

.markmap-foreign {
  font-weight: bold;
}

/* Toolbar styles */
.mm-toolbar {
  @apply bg-white dark:bg-gray-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 !important;
}

.mm-toolbar > button {
  @apply text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 !important;
}

.mm-toolbar .mm-toolbar-item {
  cursor: pointer;
  padding: 3px;
}

.mm-toolbar .mm-toolbar-item:nth-child(4) {
  display: none;
}

.mm-toolbar > button:disabled {
  @apply opacity-50 cursor-not-allowed !important;
}

/* Dark mode support */
:root[class~="dark"] .markmap-node > circle {
  stroke: #1e293b;
}

:root[class~="dark"] .markmap-node > text {
  fill: #f1f5f9;
}

:root[class~="dark"] .markmap-foreign {
  color: #f1f5f9;
}

:root[class~="dark"] .mm-toolbar .mm-toolbar-item {
  color: #fff;
}
</style>