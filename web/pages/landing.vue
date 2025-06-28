<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <!-- Hero Section -->
    <div class="relative min-h-screen flex flex-col items-center justify-center px-6 py-24">
      <div class="max-w-5xl mx-auto text-center">
        <h1 class="text-5xl sm:text-7xl font-bold bg-gradient-to-r from-primary-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent mb-6">
          Analyze the Unstructured.
        </h1>
        <p class="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 mb-8">
          From text to video — AI-driven insights and teamwork.
        </p>

        <!-- Animated Prompts -->
        <div class="relative h-12 mb-12 overflow-hidden">
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="text-lg sm:text-xl text-gray-500 dark:text-gray-400 font-mono">
              <span class="text-primary-600 dark:text-primary-400">></span>
              <span ref="promptText" class="typing-text"></span>
              <span class="animate-pulse">|</span>
            </div>
          </div>
        </div>

        <!-- CTAs -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
          <button class="px-8 py-4 rounded-xl bg-primary-600 text-white text-lg font-medium hover:bg-primary-700 transition-colors shadow-lg hover:shadow-xl hover:shadow-primary-600/20">
            Try DeepCite Now
          </button>
          <button class="px-8 py-4 rounded-xl bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-lg font-medium border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors shadow-lg hover:shadow-xl">
            Explore Public Spaces
          </button>
        </div>

        <!-- File Upload Area -->
        <div class="max-w-2xl mx-auto">
          <div class="relative rounded-2xl border-2 border-dashed border-gray-300/60 dark:border-gray-600/60 p-8 text-center hover:border-primary-500 dark:hover:border-primary-400 transition-all duration-200 group">
            <div class="absolute inset-0 bg-gradient-to-r from-primary-500/5 to-purple-500/5 rounded-2xl"></div>
            <div class="relative flex flex-col items-center">
              <UploadCloud class="h-12 w-12 text-primary-500 dark:text-primary-400 transition-transform duration-200 group-hover:scale-110 mb-4" />
              <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                Drop your files here
              </h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                or click to browse
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <!-- Model Section -->
    <div class="py-24 px-6 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm border-y border-gray-200/60 dark:border-gray-700/60">
      <div class="max-w-7xl mx-auto">
        <div class="relative">
          <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-3xl opacity-10"></div>
          <div class="relative p-8 sm:p-12 rounded-3xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
            <div class="max-w-3xl mx-auto text-center">
              <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400 text-sm font-medium mb-6">
                <Cpu class="h-4 w-4"/>
                Powered by deepcite-text-v1
              </div>
              <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-6">
                Purpose-Built for Deep Document Analysis
              </h2>
              <p class="text-lg text-gray-600 dark:text-gray-300 mb-8">
                Our specialized language model is built from the ground up to excel at document comprehension and analysis. It understands context, maintains accuracy, and provides verifiable insights from your documents.
              </p>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="p-6 rounded-xl bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
                  <div class="h-10 w-10 rounded-lg bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center mb-4">
                    <Brain class="h-5 w-5 text-blue-600 dark:text-blue-400"/>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Context-Aware</h3>
                  <p class="text-sm text-gray-600 dark:text-gray-300">
                    Understands document structure, relationships, and cross-references for deeper insights.
                  </p>
                </div>
                <div class="p-6 rounded-xl bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
                  <div class="h-10 w-10 rounded-lg bg-purple-100 dark:bg-purple-900/50 flex items-center justify-center mb-4">
                    <Target class="h-5 w-5 text-purple-600 dark:text-purple-400"/>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">99.9% Accurate</h3>
                  <p class="text-sm text-gray-600 dark:text-gray-300">
                    Every response is grounded in your documents with precise citations and evidence.
                  </p>
                </div>
                <div class="p-6 rounded-xl bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
                  <div class="h-10 w-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center mb-4">
                    <Zap class="h-5 w-5 text-emerald-600 dark:text-emerald-400"/>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Lightning Fast</h3>
                  <p class="text-sm text-gray-600 dark:text-gray-300">
                    Optimized for speed with advanced caching and parallel processing capabilities.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="py-24 px-6">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="feature in features" :key="feature.title" class="relative group">
            <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-2xl opacity-10 group-hover:opacity-20 transition-opacity"></div>
            <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
              <div class="h-12 w-12 rounded-xl bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center mb-6">
                <component :is="feature.icon" class="h-6 w-6 text-primary-600 dark:text-primary-400" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
                {{ feature.title }}
              </h3>
              <p class="text-gray-600 dark:text-gray-300">
                {{ feature.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm border-t border-gray-200/60 dark:border-gray-700/60 py-12">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex flex-wrap items-center justify-center gap-8 text-sm text-gray-500 dark:text-gray-400">
          <NuxtLink to="/about" class="hover:text-gray-900 dark:hover:text-gray-100 transition-colors">About</NuxtLink>
          <NuxtLink to="/my-subscription" class="hover:text-gray-900 dark:hover:text-gray-100 transition-colors">Pricing</NuxtLink>
          <NuxtLink to="/spaces" class="hover:text-gray-900 dark:hover:text-gray-100 transition-colors">Public Spaces</NuxtLink>
          <NuxtLink to="/terms" class="hover:text-gray-900 dark:hover:text-gray-100 transition-colors">Terms</NuxtLink>
          <NuxtLink to="/privacy" class="hover:text-gray-900 dark:hover:text-gray-100 transition-colors">Privacy</NuxtLink>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  UploadCloud, FileText, Video, Music, Image, Database, FileSpreadsheet,
  Brain, Layout, MessageSquare, Cpu, Target, Zap
} from 'lucide-vue-next'

const prompts = [
  'Summarize this 25-page PDF',
  'What are the key findings from this video?',
  'Extract insights from a scanned research poster',
  'Compare two studies from different formats',
  'Generate citations from these interview recordings'
]

const fileTypes = [
  { name: 'Text & PDF', icon: FileText },
  { name: 'Video', icon: Video },
  { name: 'Audio', icon: Music },
  { name: 'Images', icon: Image },
  { name: 'Spreadsheets', icon: FileSpreadsheet },
  { name: 'Databases', icon: Database }
]

const features = [
  {
    title: 'Understand Any Format',
    description: 'From PDFs to videos, extract insights from any type of content with our advanced AI analysis.',
    icon: Brain
  },
  {
    title: 'Spaces for Collaboration',
    description: 'Create public or private spaces to collaborate with your team and share knowledge effectively.',
    icon: Layout
  },
  {
    title: 'Ask, Analyze, Act',
    description: 'Ask natural questions, get precise answers with citations, and take action with confidence.',
    icon: MessageSquare
  }
]

const promptText = ref<HTMLElement | null>(null)
let currentPromptIndex = 0
let currentCharIndex = 0
let typingInterval: NodeJS.Timeout | null = null

const typePrompt = () => {
  if (!promptText.value) return

  const currentPrompt = prompts[currentPromptIndex]
  if (currentCharIndex < currentPrompt.length) {
    promptText.value.textContent = currentPrompt.substring(0, currentCharIndex + 1)
    currentCharIndex++
  } else {
    // Pause at the end of the prompt before erasing
    setTimeout(() => {
      erasePrompt()
    }, 2000)
  }
}

const erasePrompt = () => {
  if (!promptText.value) return

  const currentText = promptText.value.textContent || ''
  if (currentText.length > 0) {
    promptText.value.textContent = currentText.substring(0, currentText.length - 1)
    setTimeout(erasePrompt, 50)
  } else {
    currentPromptIndex = (currentPromptIndex + 1) % prompts.length
    currentCharIndex = 0
    setTimeout(() => {
      if (typingInterval) clearInterval(typingInterval)
      typingInterval = setInterval(typePrompt, 100)
    }, 500)
  }
}

onMounted(() => {
  typingInterval = setInterval(typePrompt, 100)
})

onUnmounted(() => {
  if (typingInterval) clearInterval(typingInterval)
})

definePageMeta({
  layout: 'header'
})
</script>

<style scoped>
.typing-text {
  display: inline-block;
  min-width: 1ch;
}
</style>