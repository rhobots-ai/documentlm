<template>
  <div class="bg-white dark:bg-gray-900 rounded-lg border-2 shadow-sm p-6 relative transition-all"
       :class="[
         isCurrentPlan
           ? 'border-primary-500 dark:border-primary-400 ring-1 ring-primary-500 dark:ring-primary-400'
           : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
       ]"
  >
    <!-- Plan Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <h3 class="text-lg font-medium" :class="priceColor">{{ name }}</h3>
      </div>
    </div>

    <div class="my-4 text-sm text-gray-600 dark:text-gray-300">
      {{ description }}
    </div>

    <!-- Tokens -->
    <div class="mb-6 bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
      <div class="text-2xl font-bold mb-1 text-gray-900 dark:text-gray-100">
        {{ formatNumberCompact(tokens, 0) }} tokens
      </div>
      <div class="text-sm text-gray-500 dark:text-gray-400">
        every month
      </div>
    </div>

    <!-- Price -->
    <div class="mb-6">
      <div class="text-2xl font-bold" :class="priceColor">
        ${{ price / 100 }}
      </div>
      <div class="text-sm text-gray-500 dark:text-gray-400">
        per {{ isAnnual ? 'year' : 'month' }}
      </div>
    </div>

    <!-- Action Button -->
    <button
        class="w-full px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        :class="[
          isCurrentPlan
            ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400 border border-primary-200 dark:border-primary-700'
            : buttonClasses
        ]"
        :disabled="isCurrentPlan || isLoading"
        @click="handleUpgrade"
    >
      <template v-if="isCurrentPlan">Current Plan</template>
      <template v-else-if="isLoading">
        <div class="flex items-center justify-center gap-2">
          <Loader2 class="h-4 w-4 animate-spin" />
          <span>Processing...</span>
        </div>
      </template>
      <template v-else>
        {{ price > currentPrice || activeSubscription.status != 'active' ? `Upgrade to ${name}` : `Downgrade to ${name}` }}
      </template>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { formatNumberCompact } from "~/utils/size";
import { Loader2 } from 'lucide-vue-next'

const subscriptionsStore = useSubscriptionsStore()
const { activeSubscription } = storeToRefs(subscriptionsStore)
const isLoading = ref(false)

const currentPrice = computed(() => activeSubscription.value?.plan?.amount || 0)

const props = defineProps<{
  name: string
  price: number
  tokens: number
  description: string
  isCurrentPlan?: boolean
  color?: string
  isAnnual: boolean
  id: string
}>()

defineEmits<{
  (e: 'action'): void
}>()

const handleUpgrade = async () => {
  isLoading.value = true
  try {
    const subscription = await subscriptionsStore.createNewSubscription(props.id)
    if (subscription?.gateway_short_url) {
      window.open(subscription.gateway_short_url, '_blank')
    }
  } catch (error) {
    console.error('Error creating subscription:', error)
  } finally {
    isLoading.value = false
  }
}

const priceColor = computed(() => {
  switch (props.color) {
    case 'purple':
      return 'text-purple-600 dark:text-purple-400'
    case 'emerald':
      return 'text-emerald-600 dark:text-emerald-400'
    default:
      return 'text-gray-900 dark:text-gray-100'
  }
})

const buttonClasses = computed(() => {
  if (props.isCurrentPlan) {
    return 'border border-primary-300 dark:border-primary-600 text-primary-700 dark:text-primary-300 hover:bg-primary-50 dark:hover:bg-primary-900/50'
  }

  switch (props.color) {
    case 'purple':
      return 'bg-purple-600 text-white hover:bg-purple-700'
    case 'emerald':
      return 'bg-emerald-600 text-white hover:bg-emerald-700'
    default:
      return 'bg-primary-600 text-white hover:bg-primary-700'
  }
})
</script>