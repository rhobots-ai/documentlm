<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-6xl font-bold bg-gradient-to-r from-primary-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
          Terms and Conditions
        </h1>
        <p class="mt-6 text-xl text-gray-600 dark:text-gray-300">
          Please read these terms carefully before using DocumentLM.
        </p>
      </div>

      <!-- Terms Content -->
      <div class="relative">
        <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-2xl opacity-10"></div>
        <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
          <div class="prose prose-lg dark:prose-invert max-w-none">
            <!-- Service Terms -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">1. Terms of Service</h2>
            <p class="text-gray-600 dark:text-gray-300">
              By accessing and using DocumentLM, you agree to be bound by these terms and conditions, all applicable laws and regulations, and agree that you are responsible for compliance with any applicable local laws.
            </p>

            <!-- Use License -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">2. Use License</h2>
            <p class="text-gray-600 dark:text-gray-300">
              Permission is granted to temporarily access DocumentLM for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Modify or copy the materials</li>
              <li>Use the materials for any commercial purpose</li>
              <li>Attempt to decompile or reverse engineer any software contained in DocumentLM</li>
              <li>Remove any copyright or other proprietary notations from the materials</li>
            </ul>

            <!-- Data Privacy -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">3. Data Privacy</h2>
            <p class="text-gray-600 dark:text-gray-300">
              Your use of DocumentLM is also governed by our Privacy Policy. The documents you upload are processed securely and are not shared with third parties without your explicit consent.
            </p>

            <!-- API Usage -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">4. API Usage</h2>
            <p class="text-gray-600 dark:text-gray-300">
              If you're using our API services, you agree to:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Not exceed the rate limits</li>
              <li>Keep your API keys secure</li>
              <li>Not share or redistribute API access</li>
              <li>Use the API in accordance with our documentation</li>
            </ul>

            <!-- Disclaimer -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">5. Disclaimer</h2>
            <p class="text-gray-600 dark:text-gray-300">
              The materials on DocumentLM are provided on an 'as is' basis. DocumentLM makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
            </p>

            <!-- Updates -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">6. Terms Updates</h2>
            <p class="text-gray-600 dark:text-gray-300">
              DocumentLM may revise these terms of service at any time without notice. By using this website you are agreeing to be bound by the then current version of these terms of service.
            </p>

            <!-- Contact -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">7. Contact Us</h2>
            <p class="text-gray-600 dark:text-gray-300">
              If you have any questions about these Terms, please contact us at:
            </p>
            <div class="flex items-center gap-2 text-primary-600 dark:text-primary-400">
              <Mail class="h-5 w-5" />
              <a href="mailto:tech@rhobots.ai" class="hover:underline">tech@rhobots.ai</a>
            </div>

            <!-- Last Updated -->
            <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Last updated: May 9, 2025
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Mail } from 'lucide-vue-next'

definePageMeta({
  layout: 'header'
})
</script>