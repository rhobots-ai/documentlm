<template>
  <div class="p-6">
    <div class="max-w-4xl mx-auto">
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Platform</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Manage your API keys and billing settings</p>
      </div>

      <!-- API Keys Section -->
      <PlatformKeys class="mb-8"/>

      <!-- Billing Section -->
      <PlatformBilling />
    </div>
  </div>
</template>

<script setup lang="ts">
import PlatformBilling from '~/components/platform/Billing.vue'


definePageMeta({
  layout: 'header'
})

</script>