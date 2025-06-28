<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
      <!-- Hero Section -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-6xl font-bold bg-gradient-to-r from-primary-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
          The Future of Document Intelligence
        </h1>
        <p class="mt-6 text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto relative">
          Powered by
          <span class="relative inline-block">
            <span class="text-primary-600 dark:text-primary-400 font-semibold">deepcite-text-v1</span>
            <svg class="absolute -bottom-4 left-0 w-full" viewBox="0 0 100 15" preserveAspectRatio="none">
              <path d="M0,5 Q25,3 50,5 T100,5" fill="none" stroke="currentColor" stroke-width="2" class="text-primary-400/50 dark:text-primary-600/50" />
            </svg>
          </span>
          , our purpose-built model for understanding and interacting with documents at a deeper level.
        </p>
      </div>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        <!-- Feature 1 -->
        <div class="relative group">
          <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-2xl opacity-10 group-hover:opacity-20 transition-opacity"></div>
          <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
            <div class="h-12 w-12 rounded-xl bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center mb-6">
              <Brain class="h-6 w-6 text-primary-600 dark:text-primary-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
              Contextual Understanding
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Our model understands document context, relationships, and nuances, enabling more meaningful interactions.
            </p>
          </div>
        </div>

        <!-- Feature 2 -->
        <div class="relative group">
          <div class="absolute inset-0 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-2xl opacity-10 group-hover:opacity-20 transition-opacity"></div>
          <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
            <div class="h-12 w-12 rounded-xl bg-purple-100 dark:bg-purple-900/50 flex items-center justify-center mb-6">
              <MessageSquare class="h-6 w-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
              Natural Conversations
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Engage in natural, flowing conversations about your documents with precise, contextual responses.
            </p>
          </div>
        </div>

        <!-- Feature 3 -->
        <div class="relative group">
          <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-primary-500 rounded-2xl opacity-10 group-hover:opacity-20 transition-opacity"></div>
          <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
            <div class="h-12 w-12 rounded-xl bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center mb-6">
              <BookOpen class="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
              Citation Tracking
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Every insight is backed by precise citations, ensuring transparency and accuracy in document analysis.
            </p>
          </div>
        </div>
      </div>

      <!-- Model Section -->
      <div class="relative rounded-3xl overflow-hidden mb-16">
        <div class="absolute inset-0 bg-gradient-to-r from-primary-600 via-purple-600 to-indigo-600 opacity-10"></div>
        <div class="relative p-8 sm:p-12 backdrop-blur-sm">
          <div class="max-w-3xl mx-auto text-center">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-6">
              Meet deepcite-text-v1
            </h2>
            <p class="text-lg text-gray-600 dark:text-gray-300 mb-8">
              Our specialized language model is built from the ground up to excel at document comprehension and analysis. It understands context, maintains accuracy, and provides verifiable insights from your documents.
            </p>
            <div class="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-primary-600 text-white text-lg font-medium hover:bg-primary-700 transition-colors">
              <FileText class="h-5 w-5" />
              Try it with your documents
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Section -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="text-center p-6 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
          <div class="text-4xl font-bold text-primary-600 dark:text-primary-400 mb-2">99.9%</div>
          <div class="text-sm text-gray-600 dark:text-gray-300">Citation Accuracy</div>
        </div>
        <div class="text-center p-6 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
          <div class="text-4xl font-bold text-purple-600 dark:text-purple-400 mb-2">150+</div>
          <div class="text-sm text-gray-600 dark:text-gray-300">File Formats Supported</div>
        </div>
        <div class="text-center p-6 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
          <div class="text-4xl font-bold text-indigo-600 dark:text-indigo-400 mb-2">10M+</div>
          <div class="text-sm text-gray-600 dark:text-gray-300">Documents Analyzed</div>
        </div>
      </div>

      <!-- Company Details Footer -->
      <div v-if="false" class="mt-16 text-center text-sm text-gray-400 dark:text-gray-500 space-y-1">
        <p>MAYVIONAI INTELLIGENCE PRIVATE LIMITED</p>
        <p>CIN: U62090HR2024PTC126993</p>
        <p>628, 2ND FLOOR, SECTOR 9A, NEKI RAM MARG</p>
        <p>Gurgaon, Sadar Bazar, Gurgaon- 122001, Haryana</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Brain, MessageSquare, BookOpen, FileText } from 'lucide-vue-next'

definePageMeta({
  layout: 'header'
})
</script>