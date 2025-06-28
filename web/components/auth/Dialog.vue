<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" @close="$emit('close')" class="relative z-50">
      <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/30 backdrop-blur-sm"/>
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-xl bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
              <!-- Logo -->
              <div class="text-center mb-6">
                <img
                    :src="isDark ? '/images/logo-dark.svg' : '/images/logo-light.svg'"
                    alt="Logo"
                    class="h-8 mx-auto"
                />
              </div>

              <!-- Tabs -->
              <div class="flex border-b border-gray-200 dark:border-gray-700 mb-6">
                <button
                    class="px-4 py-2 text-sm font-medium transition-colors relative"
                    :class="activeTab === 'signin' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'"
                    @click="activeTab = 'signin'"
                >
                  Sign In
                  <div
                      class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600 dark:bg-primary-400 transform origin-left transition-transform"
                      :class="activeTab === 'signin' ? 'scale-x-100' : 'scale-x-0'"
                  />
                </button>
                <button
                    class="px-4 py-2 text-sm font-medium transition-colors relative"
                    :class="activeTab === 'signup' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'"
                    @click="activeTab = 'signup'"
                >
                  Sign Up
                  <div
                      class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600 dark:bg-primary-400 transform origin-left transition-transform"
                      :class="activeTab === 'signup' ? 'scale-x-100' : 'scale-x-0'"
                  />
                </button>
              </div>

              <!-- Sign In Form -->
              <form v-if="activeTab === 'signin'" @submit.prevent="handleSignIn" class="space-y-4">
                <!-- Email -->
                <div>
                  <label for="signin-email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Email
                  </label>
                  <input
                      id="signin-email"
                      autocomplete="email"
                      v-model="signInForm.email"
                      type="email"
                      required
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': formErrors.email }"
                  />
                  <p v-if="formErrors.email" class="mt-1 text-xs text-red-500">{{ formErrors.email }}</p>
                </div>

                <!-- Password -->
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label for="signin-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Password
                    </label>
                    <button
                        type="button"
                        class="text-xs text-primary-600 dark:text-primary-400 hover:underline"
                        @click="showForgotPassword = true"
                    >
                      Forgot password?
                    </button>
                  </div>
                  <div class="relative">
                    <input
                        id="signin-password"
                        autocomplete="current-password"
                        v-model="signInForm.password"
                        :type="showPassword ? 'text' : 'password'"
                        required
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500 pr-10"
                        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': formErrors.password }"
                    />
                    <button
                        type="button"
                        class="absolute inset-y-0 right-0 pr-3 flex items-center"
                        @click="showPassword = !showPassword"
                    >
                      <Eye v-if="showPassword" class="h-5 w-5 text-gray-400"/>
                      <EyeOff v-else class="h-5 w-5 text-gray-400"/>
                    </button>
                  </div>
                  <p v-if="formErrors.password" class="mt-1 text-xs text-red-500">{{ formErrors.password }}</p>
                </div>

                <!-- Remember Me -->
                <div class="flex items-center">
                  <input
                      id="remember-me"
                      v-model="signInForm.rememberMe"
                      type="checkbox"
                      class="h-4 w-4 rounded border-gray-300 dark:border-gray-600 text-primary-600 dark:text-primary-400 focus:ring-primary-500"
                  />
                  <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                    Remember me
                  </label>
                </div>

                <!-- Error Message -->
                <div v-if="authError" class="p-3 rounded-lg bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-sm">
                  {{ authError }}
                </div>

                <!-- Signup Success Message -->
                <div v-if="signUpSuccess" class="p-3 rounded-lg bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm">
                  <div class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    <div>
                      <p class="font-medium">Account created successfully!</p>
                      <p class="text-xs mt-1">Please check your email to verify your account before signing in.</p>
                    </div>
                  </div>
                </div>

                <!-- Submit Button -->
                <button
                    type="submit"
                    class="w-full px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors flex items-center justify-center"
                    :disabled="isLoading"
                >
                  <Loader2 v-if="isLoading" class="h-4 w-4 mr-2 animate-spin"/>
                  Sign In
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

                <!-- Social Login Buttons -->
                <div class="grid grid-cols-1 gap-3">
                  <AuthSocial/>
                </div>
              </form>

              <!-- Sign Up Form -->
              <form v-if="activeTab === 'signup'" @submit.prevent="handleSignUp" class="space-y-4">
                <!-- Full Name -->
                <div>
                  <label for="signup-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Full Name
                  </label>
                  <input
                      id="signup-name"
                      v-model="signUpForm.name"
                      type="text"
                      required
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': formErrors.name }"
                  />
                  <p v-if="formErrors.name" class="mt-1 text-xs text-red-500">{{ formErrors.name }}</p>
                </div>

                <!-- Email -->
                <div>
                  <label for="signup-email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Email
                  </label>
                  <input
                      id="signup-email"
                      v-model="signUpForm.email"
                      type="email"
                      required
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': formErrors.email }"
                  />
                  <p v-if="formErrors.email" class="mt-1 text-xs text-red-500">{{ formErrors.email }}</p>
                </div>

                <!-- Password -->
                <div>
                  <label for="signup-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Password
                  </label>
                  <div class="relative">
                    <input
                        id="signup-password"
                        v-model="signUpForm.password"
                        :type="showPassword ? 'text' : 'password'"
                        required
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500 pr-10"
                        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': formErrors.password }"
                    />
                    <button
                        type="button"
                        class="absolute inset-y-0 right-0 pr-3 flex items-center"
                        @click="showPassword = !showPassword"
                    >
                      <Eye v-if="showPassword" class="h-5 w-5 text-gray-400"/>
                      <EyeOff v-else class="h-5 w-5 text-gray-400"/>
                    </button>
                  </div>
                  <p v-if="formErrors.password" class="mt-1 text-xs text-red-500">{{ formErrors.password }}</p>
                </div>

                <!-- Password Strength Indicator -->
                <div v-if="signUpForm.password">
                  <div class="flex items-center gap-2 mb-1">
                    <div class="h-1 flex-1 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
                      <div
                          class="h-full transition-all duration-300"
                          :class="[
                          passwordStrength === 'weak' ? 'w-1/3 bg-red-500' :
                          passwordStrength === 'medium' ? 'w-2/3 bg-yellow-500' :
                          'w-full bg-green-500'
                        ]"
                      ></div>
                    </div>
                    <span class="text-xs" :class="[
                      passwordStrength === 'weak' ? 'text-red-500' :
                      passwordStrength === 'medium' ? 'text-yellow-500' :
                      'text-green-500'
                    ]">
                      {{ passwordStrength === 'weak' ? 'Weak' : passwordStrength === 'medium' ? 'Medium' : 'Strong' }}
                    </span>
                  </div>
                  <ul class="text-xs space-y-1 text-gray-500 dark:text-gray-400">
                    <li class="flex items-center gap-1">
                      <Check v-if="passwordCriteria.length" class="h-3 w-3 text-green-500"/>
                      <X v-else class="h-3 w-3 text-red-500"/>
                      At least 8 characters
                    </li>
                    <li class="flex items-center gap-1">
                      <Check v-if="passwordCriteria.uppercase" class="h-3 w-3 text-green-500"/>
                      <X v-else class="h-3 w-3 text-red-500"/>
                      Contains uppercase letter
                    </li>
                    <li class="flex items-center gap-1">
                      <Check v-if="passwordCriteria.number" class="h-3 w-3 text-green-500"/>
                      <X v-else class="h-3 w-3 text-red-500"/>
                      Contains number
                    </li>
                  </ul>
                </div>

                <!-- Error Message -->
                <div v-if="authError" class="p-3 rounded-lg bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-sm">
                  {{ authError }}
                </div>

                <!-- Submit Button -->
                <button
                    type="submit"
                    class="w-full px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors flex items-center justify-center"
                    :disabled="isLoading"
                >
                  <Loader2 v-if="isLoading" class="h-4 w-4 mr-2 animate-spin"/>
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

                <!-- Social Login Buttons -->
                <div class="grid grid-cols-1 gap-3">
                  <AuthSocial/>
                </div>

                <!-- Terms Agreement -->
                <p class="text-xs text-center text-gray-500 dark:text-gray-400">
                  By signing up, you agree to our
                  <NuxtLink to="/terms" class="text-primary-600 dark:text-primary-400 hover:underline">Terms of Service</NuxtLink>
                  and
                  <NuxtLink to="/privacy" class="text-primary-600 dark:text-primary-400 hover:underline">Privacy Policy</NuxtLink>
                </p>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>

  <!-- Forgot Password Dialog -->
  <TransitionRoot appear :show="showForgotPassword" as="template">
    <Dialog as="div" @close="showForgotPassword = false" class="relative z-50">
      <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/30 backdrop-blur-sm"/>
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-xl bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
              <div class="flex justify-between items-center mb-4">
                <DialogTitle as="h3" class="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Reset Password
                </DialogTitle>
                <button
                    type="button"
                    class="text-gray-400 hover:text-gray-500"
                    @click="showForgotPassword = false"
                >
                  <X class="h-5 w-5"/>
                </button>
              </div>

              <form @submit.prevent="handleForgotPassword" class="space-y-4">
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  Enter your email address and we'll send you a link to reset your password.
                </p>

                <!-- Email -->
                <div>
                  <label for="reset-email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Email
                  </label>
                  <input
                      id="reset-email"
                      v-model="forgotPasswordEmail"
                      type="email"
                      required
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>

                <!-- Success Message -->
                <div v-if="resetEmailSent" class="p-3 rounded-lg bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm">
                  Password reset link sent! Please check your email.
                </div>

                <!-- Submit Button -->
                <div class="flex justify-end gap-3">
                  <button
                      type="button"
                      class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                      @click="showForgotPassword = false"
                  >
                    Cancel
                  </button>
                  <button
                      type="submit"
                      class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors flex items-center"
                      :disabled="isLoading || resetEmailSent"
                  >
                    <Loader2 v-if="isLoading" class="h-4 w-4 mr-2 animate-spin"/>
                    {{ resetEmailSent ? 'Sent' : 'Send Reset Link' }}
                  </button>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {Check, Eye, EyeOff, Loader2, X} from 'lucide-vue-next'
import {useWhiteLabeled} from "~/composables/useWhiteLabeled";
import {process} from "std-env";

const props = defineProps<{
  show: boolean
  initialTab?: 'signin' | 'signup'
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'success'): void
}>()

const isDark = ref(false)
const callbackURL = ref('')
const activeTab = ref(props.initialTab || 'signin')
const showPassword = ref(false)
const isLoading = ref(false)
const authError = ref('')
const signUpSuccess = ref<boolean>(false)
const showForgotPassword = ref(false)
const forgotPasswordEmail = ref('')
const resetEmailSent = ref(false)
const {getCurrentHost} = useWhiteLabeled()

// Form data
const signInForm = ref({
  email: '',
  password: '',
  rememberMe: false
})

const signUpForm = ref({
  name: '',
  email: '',
  password: ''
})

// Form validation
const formErrors = ref({
  name: '',
  email: '',
  password: ''
})

// Password strength
const passwordCriteria = computed(() => {
  const password = signUpForm.value.password
  return {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    number: /[0-9]/.test(password)
  }
})

const passwordStrength = computed(() => {
  const criteria = passwordCriteria.value
  const score = Object.values(criteria).filter(Boolean).length

  if (score <= 1) return 'weak'
  if (score === 2) return 'medium'
  return 'strong'
})

// Watch for prop changes
watch(() => props.initialTab, (newTab) => {
  if (newTab) {
    activeTab.value = newTab
  }
})

// Watch for dark mode
onMounted(() => {
  // Check for saved theme preference or system preference
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  isDark.value = savedTheme === 'dark' || (!savedTheme && prefersDark)

  callbackURL.value = getCurrentHost() + '/auth'
})

// Auth client
const {signIn, signUp} = useAuthClient()

// Handle sign in
const handleSignIn = async () => {
  // Reset errors
  authError.value = ''
  signUpSuccess.value = false
  formErrors.value = {name: '', email: '', password: ''}

  // Validate form
  if (!validateEmail(signInForm.value.email)) {
    formErrors.value.email = 'Please enter a valid email address'
    return
  }

  isLoading.value = true

  try {
    const {error} = await signIn.email({
      email: signInForm.value.email,
      password: signInForm.value.password,
      rememberMe: signInForm.value.rememberMe,
      callbackURL: callbackURL.value
    })

    if (error) throw error

    emit('success')
    emit('close')
  } catch (error: any) {
    authError.value = error.message
  } finally {
    isLoading.value = false
  }
}

// Handle sign up
const handleSignUp = async () => {
  // Reset errors
  authError.value = ''
  signUpSuccess.value = false
  formErrors.value = {name: '', email: '', password: ''}

  // Validate form
  if (signUpForm.value.name.length < 2) {
    formErrors.value.name = 'Name must be at least 2 characters'
    return
  }

  if (!validateEmail(signUpForm.value.email)) {
    formErrors.value.email = 'Please enter a valid email address'
    return
  }

  if (signUpForm.value.password.length < 8) {
    formErrors.value.password = 'Password must be at least 8 characters'
    return
  }

  isLoading.value = true

  try {
    const {error} = await signUp.email({
      email: signUpForm.value.email,
      password: signUpForm.value.password,
      name: signUpForm.value.name,
      callbackURL: callbackURL.value
    })

    if (error) throw error

    // Show a success message
    authError.value = ''

    // Create success alert
    activeTab.value = 'signin'
    signUpSuccess.value = true

    // Pre-fill the email in the sign-in form
    signInForm.value.email = signUpForm.value.email

    // Reset sign-up form
    signUpForm.value = {
      name: '',
      email: '',
      password: ''
    }
  } catch (error: any) {
    authError.value = error.message
  } finally {
    isLoading.value = false
  }
}

// Handle forgot password
const handleForgotPassword = async () => {
  if (!validateEmail(forgotPasswordEmail.value)) {
    return
  }

  isLoading.value = true

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    resetEmailSent.value = true

    // Close dialog after 3 seconds
    setTimeout(() => {
      showForgotPassword.value = false
      resetEmailSent.value = false
      forgotPasswordEmail.value = ''
    }, 10000)
  } catch (error) {
    console.error('Forgot password error:', error)
  } finally {
    isLoading.value = false
  }
}

// Validate email
const validateEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
</script>