<template>
  <div class="p-6">
    <div class="max-w-4xl mx-auto space-y-6">
      <!-- Header -->
      <div>
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Billing & Plans</h1>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Manage your subscription and billing details</p>
          </div>
        </div>
      </div>

      <!-- Current Plan -->
      <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
        <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div class="flex-1">
            <div class="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
              <div class="flex items-baseline gap-2">
                <span class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ formatNumberCompact(usage?.remaining) }}</span>
                <div class="flex items-center gap-2">
                  <span class="text-sm text-gray-600 dark:text-gray-300">tokens left</span>
                  <button
                      class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                      @click="refreshTokens"
                      :class="{ 'animate-spin': isRefreshing }"
                  >
                    <RefreshCw class="h-3.5 w-3.5 text-gray-400 dark:text-gray-500"/>
                  </button>
                </div>
              </div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Resets to {{ formatNumberCompact(usage?.total) }} tokens on {{ formatDate(usage?.expires_at, 1) }}</div>
              <div class="mt-2">
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-500 dark:text-gray-400">{{ usage?.used.toLocaleString() }} used</span>
                  <span class="text-gray-500 dark:text-gray-400">{{ usage?.total.toLocaleString() }} total</span>
                </div>
                <div class="mt-2 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                      class="h-full bg-primary-500 dark:bg-primary-400 rounded-full transition-all"
                      :style="{ width: `${(usage?.used / usage?.total) * 100}%` }"
                  />
                </div>
              </div>
            </div>
            <div class="mt-4">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {{ isFreePlan ? 'Free Plan' : currentPlan?.name }}
                </span>
                <span v-if="activeSubscription && activeSubscription?.status === 'active'"
                      class="px-2 py-0.5 rounded-full text-xs font-medium bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400">
                  Active
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-300">Need more tokens?</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">Upgrade your plan below</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Plan Comparison -->
      <div>
        <!-- Billing Toggle -->
        <div class="flex items-center justify-end gap-3 bg-gray-50 dark:bg-gray-800 rounded-lg p-2 mb-6">
          <span class="text-sm text-gray-600 dark:text-gray-300">Monthly</span>
          <button
              class="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200 dark:bg-gray-700"
              :class="{ 'bg-primary-600 dark:bg-primary-500': isAnnual }"
              @click="isAnnual = !isAnnual"
          >
              <span
                  class="inline-block h-4 w-4 transform rounded-full bg-white transition"
                  :class="{ 'translate-x-6': isAnnual, 'translate-x-1': !isAnnual }"
              />
          </button>
          <span class="text-sm text-gray-600 dark:text-gray-300">
              Annual
              <span class="text-xs text-primary-600 dark:text-primary-400">(Save 10%)</span>
            </span>
        </div>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <template v-if="!loading">
            <BillingPlanCard
                v-for="plan in displayPlans"
                :key="plan.id"
                :name="plan.name"
                :price="plan.amount"
                :tokens="plan.tokens"
                :description="plan.description"
                :is-current-plan="currentPlan && currentPlan.id === plan.id && activeSubscription.status == 'active'"
                :is-annual="isAnnual"
                :id="plan.gateway_plan_id"
            />
          </template>
          <template v-else>
            <div v-for="i in 3" :key="i" class="animate-pulse">
              <div class="h-64 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
            </div>
          </template>
        </div>
      </div>

      <!-- Enterprise Plans -->
      <div class="text-center">
        <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">Looking for Enterprise plans?</h2>
        <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Contact us for custom pricing and features tailored to your organization's needs.</p>
        <a
            href="/enterprise-contact"
            target="_blank"
            class="inline-flex items-center gap-2 mt-4 px-6 py-2 rounded-lg bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-sm font-medium hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors"
        >
          <Building2 class="h-4 w-4"/>
          Contact for Quote
        </a>
      </div>

      <!-- FAQ Section -->
      <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
        <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Frequently asked questions</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">Everything you need to know about the product and billing.</p>

        <div class="space-y-4">
          <Disclosure v-slot="{ open }" as="div" class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <DisclosureButton class="flex w-full items-center justify-between text-left">
              <span class="text-sm font-medium text-gray-900 dark:text-gray-100">What are tokens?</span>
              <ChevronDown
                  class="h-5 w-5 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': open }"
              />
            </DisclosureButton>
            <DisclosurePanel class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              AI tokens are a complex topic related to all AI apps, not just Bolt. You can learn more about tokens here. For Bolt specifically it is important
              to know that most token usage is related to syncing your project's file system to the AI: the larger the project, the more tokens used per
              message. Our top priority is to increase the efficiency of token usage in Bolt. We continue to make improvements so that Bolt uses fewer tokens.
            </DisclosurePanel>
          </Disclosure>

          <Disclosure v-slot="{ open }" as="div" class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <DisclosureButton class="flex w-full items-center justify-between text-left">
              <span class="text-sm font-medium text-gray-900 dark:text-gray-100">How do Teams plans work?</span>
              <ChevronDown
                  class="h-5 w-5 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': open }"
              />
            </DisclosureButton>
            <DisclosurePanel class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              Teams provide a shared workspace for users to collaborate on Bolt projects. The subscription cost for Teams is per team member. Each paid team
              member receives a monthly token allotment based on the subscription tier. Tokens are not shared among team members. You can read more about Teams
              plans here.
            </DisclosurePanel>
          </Disclosure>

          <Disclosure v-slot="{ open }" as="div" class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <DisclosureButton class="flex w-full items-center justify-between text-left">
              <span class="text-sm font-medium text-gray-900 dark:text-gray-100">Do tokens rollover from month to month?</span>
              <ChevronDown
                  class="h-5 w-5 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': open }"
              />
            </DisclosureButton>
            <DisclosurePanel class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              Tokens associated with a paid subscription do not rollover from month to month. Tokens associated with a token reload do rollover from month to
              month, but you must have a paid subscription to use these tokens. We must reserve GPUs from our upstream inference providers that we are billed
              for regardless of whether or not they are used, which influences our token policy. By reserving these GPUs ahead of time we can negotiate better
              pricing through volume discounting. You can read more about tokens here.
            </DisclosurePanel>
          </Disclosure>

          <Disclosure v-slot="{ open }" as="div" class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <DisclosureButton class="flex w-full items-center justify-between text-left">
              <span class="text-sm font-medium text-gray-900 dark:text-gray-100">How do token reloads work?</span>
              <ChevronDown
                  class="h-5 w-5 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': open }"
              />
            </DisclosureButton>
            <DisclosurePanel class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              Token reloads are additional tokens that you can purchase as needed. Token reloads can only be used with an active subscription. Tokens associated
              with a token reload rollover.
            </DisclosurePanel>
          </Disclosure>

          <Disclosure v-slot="{ open }" as="div" class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <DisclosureButton class="flex w-full items-center justify-between text-left">
              <span class="text-sm font-medium text-gray-900 dark:text-gray-100">Can I change my plan later?</span>
              <ChevronDown
                  class="h-5 w-5 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': open }"
              />
            </DisclosureButton>
            <DisclosurePanel class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              Yes, you can change your plan by clicking Manage current plan. This will take you to our Stripe billing portal where you can select Update
              subscription to change your plan type.
            </DisclosurePanel>
          </Disclosure>

          <Disclosure v-slot="{ open }" as="div" class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <DisclosureButton class="flex w-full items-center justify-between text-left">
              <span class="text-sm font-medium text-gray-900 dark:text-gray-100">Can I cancel my subscription?</span>
              <ChevronDown
                  class="h-5 w-5 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': open }"
              />
            </DisclosureButton>
            <DisclosurePanel class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              Yes, you can cancel at any time. Click Manage current plan to be taken into the cancellation process.
            </DisclosurePanel>
          </Disclosure>

          <Disclosure v-slot="{ open }" as="div" class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <DisclosureButton class="flex w-full items-center justify-between text-left">
              <span class="text-sm font-medium text-gray-900 dark:text-gray-100">What are the token limits associated with a free plan?</span>
              <ChevronDown
                  class="h-5 w-5 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': open }"
              />
            </DisclosureButton>
            <DisclosurePanel class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              Free plans have a 150,000 token daily limit and 1 million token monthly limit.
            </DisclosurePanel>
          </Disclosure>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {Dialog, DialogPanel, DialogTitle, Disclosure, DisclosureButton, DisclosurePanel, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {Building2, ChevronDown, RefreshCw} from 'lucide-vue-next'
import {useSubscriptionsStore} from '~/stores/subscriptions'
import {useSubscriptionPlansStore} from '~/stores/subscription_plans'
import {formatNumberCompact} from "~/utils/size";

const isAnnual = ref(false)
const isRefreshing = ref(false)
const plansStore = useSubscriptionPlansStore()
const subscriptionsStore = useSubscriptionsStore()
const {monthlyPlans, annualPlans, loading} = storeToRefs(plansStore)
const {activeSubscription, usage} = storeToRefs(subscriptionsStore)

const isFreePlan = computed(() => !activeSubscription.value || activeSubscription.value?.status !== 'active')
const currentPlan = computed(() => activeSubscription.value?.plan)

watch(activeSubscription, (activeSubscriptionNewValue) => {
  isAnnual.value = activeSubscriptionNewValue.plan.interval === 'yearly'
})

// Computed plans based on billing interval
const displayPlans = computed(() => {
  return isAnnual.value ? annualPlans.value : monthlyPlans.value
})

onMounted(async () => {
  await plansStore.fetchPlans()
  await subscriptionsStore.getMySubscription()
  await subscriptionsStore.getTokenUsage()
})

const refreshTokens = async () => {
  if (isRefreshing.value) return

  isRefreshing.value = true
  try {
    await subscriptionsStore.refreshSubscription()
    await subscriptionsStore.getTokenUsage()
  } catch (error) {
    console.error('Error refreshing tokens:', error)
  } finally {
    isRefreshing.value = false
  }
}
</script>