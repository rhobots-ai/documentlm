<template>
  <div class="bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="flex items-center justify-center p-6">
      <div class="w-full max-w-md">
        <div class="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-xl shadow-lg border border-gray-200/50 dark:border-gray-700/50 p-6">
          <div v-if="!isWhiteLabeled" class="text-center mb-8">
            <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">Welcome to DeepCite</h1>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              From Text to Video—One AI for All Your Research. It helps you analyze unstructured data, extract insights, and collaborate in one powerful
              workspace.
            </p>
          </div>

          <div class="space-y-4">
            <!-- Sign In Button -->
            <button
                @click="showAuthDialog = true; authDialogTab = 'signin'"
                class="w-full px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
            >
              Sign In
            </button>

            <!-- Sign Up Button -->
            <button
                @click="showAuthDialog = true; authDialogTab = 'signup'"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              Create Account
            </button>

            <!-- Social Login Divider -->
            <div class="relative my-6">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-200 dark:border-gray-700"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-400">Or continue with</span>
              </div>
            </div>

            <AuthSocial/>
          </div>
        </div>

        <!-- Footer Links -->
        <div v-if="!isWhiteLabeled" class="mt-6 flex items-center justify-center gap-4 text-sm text-gray-400 dark:text-gray-500">
          <NuxtLink to="/about" class="hover:text-gray-600 dark:hover:text-gray-300 transition-colors">About</NuxtLink>
          <div class="h-1 w-1 rounded-full bg-gray-300 dark:bg-gray-700"></div>
          <a href="https://docs.rhobots.ai" target="_blank" class="hover:text-gray-600 dark:hover:text-gray-300 transition-colors">Docs</a>
          <div class="h-1 w-1 rounded-full bg-gray-300 dark:bg-gray-700"></div>
          <NuxtLink to="/contact" class="hover:text-gray-600 dark:hover:text-gray-300 transition-colors">Contact</NuxtLink>
          <div class="h-1 w-1 rounded-full bg-gray-300 dark:bg-gray-700"></div>
          <NuxtLink to="/privacy" class="hover:text-gray-600 dark:hover:text-gray-300 transition-colors">Privacy</NuxtLink>
          <div class="h-1 w-1 rounded-full bg-gray-300 dark:bg-gray-700"></div>
          <NuxtLink to="/terms" class="hover:text-gray-600 dark:hover:text-gray-300 transition-colors">Terms</NuxtLink>
        </div>
      </div>
    </div>

    <!-- Auth Dialog -->
    <AuthDialog
        :show="showAuthDialog"
        :initial-tab="authDialogTab"
        @close="showAuthDialog = false"
        @success="handleAuthSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {useOrganizationStore} from "~/stores/organizations";
import {storeToRefs} from "pinia";

const isDark = ref(false)
const showAuthDialog = ref(false)
const authDialogTab = ref<'signin' | 'signup'>('signin')

const organizationStore = useOrganizationStore()
const {isWhiteLabeled} = storeToRefs(organizationStore)

const userStore = useUserStore()
const {isLoggedIn} = storeToRefs(userStore)

const handleAuthSuccess = () => {
  navigateTo('/')
}

onMounted(() => {
  // Check for saved theme preference or system preference
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  isDark.value = savedTheme === 'dark' || (!savedTheme && prefersDark)

  watch(() => isLoggedIn.value, (currentIsSignedIn) => {
    if (currentIsSignedIn) {
      navigateTo('/')
    }
  }, {immediate: true})
})
</script>