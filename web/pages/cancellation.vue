<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-6xl font-bold bg-gradient-to-r from-primary-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
          Cancellation & Refund Policy
        </h1>
        <p class="mt-6 text-xl text-gray-600 dark:text-gray-300">
          Learn about our cancellation process and refund terms.
        </p>
      </div>

      <!-- Policy Content -->
      <div class="relative">
        <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-2xl opacity-10"></div>
        <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
          <div class="prose prose-lg dark:prose-invert max-w-none">
            <!-- Cancellation Terms -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">1. Cancellation Terms</h2>
            <p class="text-gray-600 dark:text-gray-300">
              When you cancel your subscription:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Your account remains active until the end of the current billing cycle</li>
              <li>You continue to have full access to all features during this period</li>
              <li>No additional charges will be made after cancellation</li>
              <li>You can reactivate your subscription at any time</li>
            </ul>

            <!-- Refund Policy -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">2. Refund Policy</h2>
            <p class="text-gray-600 dark:text-gray-300">
              Our refund policy ensures fair treatment of all customers:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Any unused portion of your payment will be refunded</li>
              <li>Refunds are processed within 5-7 business days</li>
              <li>Refund amount is calculated based on the remaining days in your billing cycle</li>
              <li>One-time setup fees or processing charges are non-refundable</li>
            </ul>
            <!-- Contact -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">5. Contact Us</h2>
            <p class="text-gray-600 dark:text-gray-300">
              For questions about cancellations or refunds, please contact our billing team:
            </p>
            <div class="flex items-center gap-2 text-primary-600 dark:text-primary-400">
              <Mail class="h-5 w-5" />
              <a href="mailto:tech@deepcite.in" class="hover:underline">tech@deepcite.in</a>
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