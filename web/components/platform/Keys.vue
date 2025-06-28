<template>

  <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
    <div class="p-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">API Keys</h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Manage your API keys for accessing the platform</p>
        </div>
        <button
            class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
            @click="showGenerateDialog = true"
        >
          <div class="flex items-center gap-2">
            <Plus class="h-4 w-4"/>
            Generate Key
          </div>
        </button>
      </div>

      <div v-if="apiKeys.length === 0" class="p-6 text-center">
        <Key class="h-12 w-12 mx-auto text-gray-400 dark:text-gray-600"/>
        <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">No API keys</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Get started by generating your first API key</p>
      </div>

      <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
        <div v-for="key in apiKeys" :key="key.digest" class="py-4">
          <div class="flex items-start justify-between gap-4">
            <div>
              <div class="flex items-center gap-2">
                <h3 class="m-0 text-sm font-medium text-gray-900 dark:text-gray-100">{{ key.name }}</h3>
                <span
                    class="px-2 py-0.5 rounded-full text-xs font-medium"
                    :class="getKeyStatus(key).class"
                >
                  {{ getKeyStatus(key).label }}
                </span>
              </div>
              <div class="mt-1 flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400">
                <span>Created {{ formatDate(key.created) }}</span>
                <span>·</span>
                <span>Expires {{ formatDate(key.expiry) }}</span>
              </div>
              <div class="mt-2 font-mono text-sm">
                <span class="text-gray-600 dark:text-gray-300">{{ key.token_key }}...</span>
              </div>
            </div>
            <button
                class="shrink-0 px-3 py-1.5 rounded-lg border border-red-200 text-red-600 text-sm font-medium hover:bg-red-50 dark:border-red-800 dark:text-red-400 dark:hover:bg-red-900/50 transition-colors"
                @click="confirmRevoke(key.digest)"
            >
              Revoke
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Generate Key Dialog -->
    <TransitionRoot appear :show="showGenerateDialog" as="template">
      <Dialog as="div" @close="showGenerateDialog = false" class="relative z-10">
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
                  Generate New API Key
                </DialogTitle>

                <form @submit.prevent="generateKey" class="space-y-4">
                  <div>
                    <label for="keyName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Key Name
                    </label>
                    <input
                        v-model="newKeyName"
                        type="text"
                        id="keyName"
                        placeholder="e.g., Development Key"
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                        required
                    />
                  </div>

                  <div>
                    <label for="expiry" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Expiry
                    </label>
                    <select
                        v-model="newKeyExpiry"
                        id="expiry"
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                    >
                      <option value="30">30 days</option>
                      <option value="90">90 days</option>
                      <option value="180">180 days</option>
                      <option value="365">1 year</option>
                      <option value="3650">10 year</option>
                    </select>
                  </div>

                  <div class="flex justify-end gap-3 mt-6">
                    <button
                        type="button"
                        class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                        @click="showGenerateDialog = false"
                    >
                      Cancel
                    </button>
                    <button
                        type="submit"
                        class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                    >
                      Generate
                    </button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Success Dialog -->
    <TransitionRoot appear :show="showSuccessDialog" as="template">
      <Dialog as="div" @close="handleSuccessClose" class="relative z-10">
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
                <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/50">
                  <Check class="h-6 w-6 text-green-600 dark:text-green-400"/>
                </div>

                <div class="mt-3 text-center">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100">
                    API Key Generated
                  </DialogTitle>

                  <div class="mt-4">
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
                      Copy your API key now. You won't be able to see it again!
                    </p>

                    <div class="relative">
                      <div class="max-w-full break-all rounded-lg bg-gray-50 dark:bg-gray-800 p-4 font-mono text-sm text-gray-900 dark:text-gray-100">
                        {{ generatedKey }}
                      </div>
                      <button
                          class="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
                          @click="copyToClipboard(generatedKey)"
                      >
                        <Copy class="h-5 w-5"/>
                      </button>
                    </div>
                  </div>
                </div>

                <div class="mt-6">
                  <button
                      class="w-full rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
                      @click="handleSuccessClose"
                  >
                    Done
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Revoke Confirmation Dialog -->
    <TransitionRoot appear :show="showRevokeDialog" as="template">
      <Dialog as="div" @close="showRevokeDialog = false" class="relative z-10">
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
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100 mb-2">
                  Revoke API Key
                </DialogTitle>

                <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
                  Are you sure you want to revoke this API key? This action cannot be undone, and any applications using this key will no longer have access.
                </p>

                <div class="flex justify-end gap-3">
                  <button
                      type="button"
                      class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                      @click="showRevokeDialog = false"
                  >
                    Cancel
                  </button>
                  <button
                      type="button"
                      class="px-4 py-2 rounded-lg bg-red-600 text-white text-sm font-medium hover:bg-red-700 transition-colors"
                      @click="handleRevoke"
                  >
                    Revoke Key
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Check, Copy, Key, Plus} from 'lucide-vue-next'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {useKeysStore} from '~/stores/keys'
import {storeToRefs} from 'pinia'

const getKeyStatus = (key: ApiKey) => {
  if (new Date(key.expiry) < new Date()) return {label: 'Expired', class: 'bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-400'}
  return {label: 'Active', class: 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-400'}
}

const keysStore = useKeysStore()
const {keys: apiKeys, loading} = storeToRefs(keysStore)

const showGenerateDialog = ref(false)
const showSuccessDialog = ref(false)
const generatedKey = ref<string | null>(null)
const newKeyName = ref('')
const newKeyExpiry = ref('30')
const keyToRevoke = ref<string | null>(null)
const showRevokeDialog = ref(false)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const generateKey = async () => {
  try {
    const key = await keysStore.createKey(newKeyName.value, parseInt(newKeyExpiry.value))
    if (key) {
      generatedKey.value = key.token // Assuming the API returns the full token in the response
      showGenerateDialog.value = false
      showSuccessDialog.value = true
    }
    newKeyName.value = ''
  } catch (error) {
    console.error('Error generating key:', error)
  }
}

const handleSuccessClose = () => {
  showSuccessDialog.value = false
  generatedKey.value = null
  keysStore.fetchKeys() // Refresh the keys list
}

const confirmRevoke = (digest: string) => {
  keyToRevoke.value = digest
  showRevokeDialog.value = true
}

const handleRevoke = async () => {
  try {
    if (keyToRevoke.value) {
      await keysStore.revokeKey(keyToRevoke.value)
    }
    showRevokeDialog.value = false
    keyToRevoke.value = null
  } catch (error) {
    console.error('Error revoking key:', error)
  }
}

const copyToClipboard = async (text: string | null) => {
  if (!text) return

  try {
    await navigator.clipboard.writeText(text)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}

onMounted(() => {
  // Fetch keys when component mounts
  keysStore.fetchKeys()
})
</script>