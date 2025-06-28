<template>
  <div class="space-y-4">
    <button
        @click="socialSignIn('google')"
        class="w-full flex items-center justify-center gap-3 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
    >
      <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" class="h-5 w-5"/>
      Continue with Google
    </button>

    <button
        type="button"
        class="w-full flex items-center justify-center gap-3 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        @click="socialSignIn('github')"
    >
      <img src="https://www.svgrepo.com/show/475654/github-color.svg" alt="Github" class="h-5 w-5"/>
      Continue with GitHub
    </button>

    <button
        type="button"
        class="w-full flex items-center justify-center gap-3 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        @click="socialSignIn('microsoft')"
    >
      <img src="https://www.svgrepo.com/show/448239/microsoft.svg" alt="Microsoft" class="h-5 w-5"/>
      Continue with Microsoft
    </button>
  </div>
</template>

<script setup lang="ts">

import {useWhiteLabeled} from "~/composables/useWhiteLabeled";

const {signIn} = useAuthClient()
const {getCurrentHost} = useWhiteLabeled()

// Handle social sign in
const socialSignIn = async (provider: 'google' | 'github' | 'microsoft') => {
  try {
    await signIn.social({
      provider,
      callbackURL: getCurrentHost() + '/auth'
    })
  } catch (error) {
    console.error('Social sign in error:', error)
  }
}
</script>