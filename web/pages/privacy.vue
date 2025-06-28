<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-6xl font-bold bg-gradient-to-r from-primary-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
          Privacy Policy
        </h1>
        <p class="mt-6 text-xl text-gray-600 dark:text-gray-300">
          Your privacy is important to us. Learn how we collect, use, and protect your data.
        </p>
      </div>

      <!-- Privacy Content -->
      <div class="relative">
        <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-2xl opacity-10"></div>
        <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
          <div class="prose prose-lg dark:prose-invert max-w-none">
            <!-- Information Collection -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">1. Information We Collect</h2>
            <p class="text-gray-600 dark:text-gray-300">
              We collect information that you provide directly to us, including:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Account information (name, email, etc.)</li>
              <li>Documents you upload for analysis</li>
              <li>Usage data and interaction with our services</li>
              <li>API usage and authentication data</li>
            </ul>

            <!-- Document Privacy -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">2. Document Privacy</h2>
            <p class="text-gray-600 dark:text-gray-300">
              Your documents are processed using our deepcite-text-v1 model with the following guarantees:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>End-to-end encryption during transmission</li>
              <li>Secure storage with industry-standard encryption</li>
              <li>No sharing with third parties without explicit consent</li>
              <li>Option to delete documents permanently</li>
            </ul>

            <!-- Data Usage -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">3. How We Use Your Data</h2>
            <p class="text-gray-600 dark:text-gray-300">
              We use the collected information for:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Providing and improving our services</li>
              <li>Processing document analysis requests</li>
              <li>Maintaining and optimizing our AI models</li>
              <li>Sending service updates and communications</li>
            </ul>

            <!-- Data Protection -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">4. Data Protection</h2>
            <p class="text-gray-600 dark:text-gray-300">
              We implement robust security measures to protect your data:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Regular security audits and penetration testing</li>
              <li>Access controls and authentication</li>
              <li>Data encryption at rest and in transit</li>
              <li>Regular backup and disaster recovery procedures</li>
            </ul>

            <!-- Cookie Policy -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">5. Cookies and Tracking</h2>
            <p class="text-gray-600 dark:text-gray-300">
              We use cookies and similar tracking technologies to:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Maintain user sessions</li>
              <li>Understand usage patterns</li>
              <li>Improve user experience</li>
              <li>Provide analytics and performance monitoring</li>
            </ul>

            <!-- Data Retention -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">6. Data Retention</h2>
            <p class="text-gray-600 dark:text-gray-300">
              We retain your data for as long as your account is active or as needed to provide services. You can request data deletion at any time through your account settings or by contacting support.
            </p>

            <!-- User Rights -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">7. Your Rights</h2>
            <p class="text-gray-600 dark:text-gray-300">
              You have the right to:
            </p>
            <ul class="text-gray-600 dark:text-gray-300">
              <li>Access your personal data</li>
              <li>Correct inaccurate data</li>
              <li>Request data deletion</li>
              <li>Export your data</li>
              <li>Opt-out of communications</li>
            </ul>

            <!-- Contact -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">8. Contact Us</h2>
            <p class="text-gray-600 dark:text-gray-300">
              For privacy-related inquiries, please contact our Data Protection Officer at:
            </p>
            <div class="flex items-center gap-2 text-primary-600 dark:text-primary-400">
              <Mail class="h-5 w-5" />
              <a href="mailto:tech@deepcite.in" class="hover:underline">tech@deepcite.in</a>
            </div>

            <!-- Updates -->
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">9. Policy Updates</h2>
            <p class="text-gray-600 dark:text-gray-300">
              We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page and updating the effective date.
            </p>

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