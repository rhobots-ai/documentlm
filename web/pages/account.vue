<template>
  <div class="p-6">
    <div v-if="profile" class="max-w-2xl mx-auto">
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Account Settings</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Manage your account preferences and personal information</p>
      </div>

      <!-- Account Label -->
      <div class="mb-6">
        <div class="flex items-center gap-2">
          <div class="px-2.5 py-1 rounded-full text-xs font-medium bg-primary-50 text-primary-700">
            Free Account
          </div>
          <NuxtLink
              v-show="false"
              to="/billing"
              class="text-xs text-primary-600 hover:text-primary-700 font-medium"
          >
            Upgrade to Pro
          </NuxtLink>
        </div>
      </div>

      <!-- Profile Section -->
      <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm divide-y divide-gray-200 dark:divide-gray-700">
        <div class="p-6">
          <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-6">Profile Information</h2>

          <div class="flex items-start gap-6">
            <!-- Profile Picture -->
            <div class="flex flex-col items-center gap-2">
              <div class="relative group">
                <div class="h-20 w-20 rounded-full bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center ring-4 ring-white dark:ring-gray-900">
                  <img
                      v-if="profile?.imageUrl"
                      :src="profile.imageUrl"
                      :alt="fullName"
                      class="h-full w-full object-cover rounded-full"
                  />
                  <User v-else class="h-8 w-8 text-primary-600"/>
                </div>
                <button
                    class="absolute inset-0 flex items-center justify-center rounded-full bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity"
                    @click="triggerFileInput"
                >
                  <Camera class="h-5 w-5 text-white"/>
                </button>
                <input
                    ref="fileInput"
                    type="file"
                    class="hidden"
                    accept="image/*"
                    @change="handleProfilePicture"
                />
              </div>
              <button
                  class="text-xs text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
                  @click="triggerFileInput"
              >
                Change photo
              </button>
            </div>

            <!-- Profile Form -->
            <form class="flex-1 space-y-4" @submit.prevent="saveProfile">
              <div>
                <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Full Name
                </label>
                <input
                    id="name"
                    v-model="fullName"
                    type="text"
                    class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                />
              </div>

              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Email Address
                </label>
                <input
                    id="email"
                    v-model="profile.email"
                    type="email"
                    class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                />
              </div>

              <div class="pt-4">
                <button
                    type="submit"
                    class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Password Section -->
        <div class="p-6">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">Password</h2>
            <button
                class="px-4 py-2 rounded-lg text-primary-600 text-sm font-medium transition-colors"
                @click="showPasswordDialog = true"
            >
              Change Password
            </button>
          </div>
        </div>
      </div>

      <!-- Password Change Dialog -->
      <TransitionRoot appear :show="showPasswordDialog" as="template">
        <Dialog as="div" @close="showPasswordDialog = false" class="relative z-10">
          <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0"
              enter-to="opacity-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100"
              leave-to="opacity-0"
          >
            <div class="fixed inset-0 bg-black/25"/>
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
                <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-lg bg-white dark:bg-gray-900 p-6 shadow-xl transition-all">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100 mb-4">
                    Change Password
                  </DialogTitle>

                  <form @submit.prevent="changePassword" class="space-y-4">
                    <div>
                      <label for="current-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Current Password
                      </label>
                      <input
                          id="current-password"
                          v-model="passwordForm.current"
                          type="password"
                          class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      />
                    </div>

                    <div>
                      <label for="new-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        New Password
                      </label>
                      <input
                          id="new-password"
                          v-model="passwordForm.new"
                          type="password"
                          class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      />
                    </div>

                    <div>
                      <label for="confirm-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Confirm New Password
                      </label>
                      <input
                          id="confirm-password"
                          v-model="passwordForm.confirm"
                          type="password"
                          class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                      />
                    </div>

                    <!-- Status Message -->
                    <div v-if="passwordChangeStatus" class="mt-3">
                      <div
                          class="flex items-center gap-2 p-3 rounded-lg text-sm"
                          :class="{
                          'bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-400': passwordChangeStatus.type === 'error',
                          'bg-green-50 dark:bg-green-900/50 text-green-700 dark:text-green-400': passwordChangeStatus.type === 'success'
                        }"
                      >
                        <component
                            :is="passwordChangeStatus.type === 'error' ? AlertCircle : CheckCircle2"
                            class="h-5 w-5 flex-shrink-0"
                        />
                        <p>{{ passwordChangeStatus.message }}</p>
                      </div>
                    </div>

                    <div class="flex justify-end gap-3 mt-6">
                      <button
                          type="button"
                          class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                          @click="showPasswordDialog = false"
                      >
                        Cancel
                      </button>
                      <button
                          type="submit"
                          class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                      >
                        Update Password
                      </button>
                    </div>
                  </form>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>
    </div>
  </div>
</template>

<script setup lang="ts">
import {AlertCircle, Camera, CheckCircle2, User} from 'lucide-vue-next'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'

const fileInput = ref<HTMLInputElement | null>(null)
const userStore = useUserStore()
const {profile, fullName} = storeToRefs(userStore)

const showPasswordDialog = ref(false)

const passwordForm = ref({
  current: '',
  new: '',
  confirm: ''
})

const passwordChangeStatus = ref<{
  type: 'success' | 'error'
  message: string
} | null>(null)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleProfilePicture = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files?.length) {
    // TODO: Implement profile picture upload
    console.log('Uploading profile picture:', input.files[0].name)
  }
}

const saveProfile = () => {
  // TODO: Implement profile update
}

const changePassword = async () => {
  if (!passwordForm.value.new || !passwordForm.value.confirm || passwordForm.value.new !== passwordForm.value.confirm) {
    passwordChangeStatus.value = {
      type: 'error',
      message: 'New passwords do not match'
    }
    return
  }

  try {
    // TODO: reset password

    // Reset form after successful change
    passwordChangeStatus.value = {
      type: 'success',
      message: 'Password updated successfully'
    }
    passwordForm.value = {
      current: '',
      new: '',
      confirm: ''
    }
    showPasswordDialog.value = false
  } catch (error: any) {
    const errorData = error.errors?.[0] || {}
    passwordChangeStatus.value = {
      type: 'error',
      message: errorData.long_message || errorData.message || 'Failed to update password'
    }
  }
}
</script>