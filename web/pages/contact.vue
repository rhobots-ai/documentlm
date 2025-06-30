<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
      <!-- Hero Section -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-6xl font-bold bg-gradient-to-r from-primary-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
          Get in Touch
        </h1>
        <p class="mt-6 text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          Have questions about DocumentLM? We're here to help you get the most out of your document analysis.
        </p>
      </div>

      <div class="max-w-4xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Contact Form -->
          <div class="relative group">
            <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-2xl opacity-10"></div>
            <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
              <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-6">Send us a message</h2>
              <form class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Name</label>
                  <input
                      type="text"
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
                  <input
                      type="email"
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Message</label>
                  <textarea
                      rows="4"
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      required
                  ></textarea>
                </div>
                <button
                    type="submit"
                    class="w-full px-6 py-3 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
                >
                  <Send class="h-4 w-4" />
                  Send Message
                </button>
              </form>
            </div>
          </div>

          <!-- Contact Info -->
          <div class="space-y-8">
            <!-- Email -->
            <div class="relative group">
              <div class="absolute inset-0 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-xl opacity-10"></div>
              <div class="relative p-6 rounded-xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
                <div class="flex items-center gap-4">
                  <div class="h-10 w-10 rounded-lg bg-purple-100 dark:bg-purple-900/50 flex items-center justify-center">
                    <Mail class="h-5 w-5 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div>
                    <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100">Email</h3>
                    <a href="mailto:tech@rhobots.ai" class="text-primary-600 dark:text-primary-400 hover:underline">
                      tech@rhobots.ai
                    </a>
                  </div>
                </div>
              </div>
            </div>

            <!-- Documentation -->
            <div class="relative group">
              <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-primary-500 rounded-xl opacity-10"></div>
              <div class="relative p-6 rounded-xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
                <div class="flex items-center gap-4">
                  <div class="h-10 w-10 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center">
                    <BookOpen class="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
                  </div>
                  <div>
                    <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100">Documentation</h3>
                    <a href="https://docs.rhobots.ai" target="_blank" class="text-primary-600 dark:text-primary-400 hover:underline">
                      docs.rhobots.ai
                    </a>
                  </div>
                </div>
              </div>
            </div>

            <!-- API Reference -->
            <div class="relative group">
              <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-xl opacity-10"></div>
              <div class="relative p-6 rounded-xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
                <div class="flex items-center gap-4">
                  <div class="h-10 w-10 rounded-lg bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
                    <Waypoints class="h-5 w-5 text-primary-600 dark:text-primary-400" />
                  </div>
                  <div>
                    <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100">API Reference</h3>
                    <a href="https://docs.rhobots.ai/api-reference" target="_blank" class="text-primary-600 dark:text-primary-400 hover:underline">
                      docs.rhobots.ai/api-reference
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Send, Mail, BookOpen, Waypoints } from 'lucide-vue-next'

definePageMeta({
  layout: 'header'
})
</script>