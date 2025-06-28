<template>
  <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
    <!-- Tabs -->
    <div>
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button
              v-for="tab in tabs"
              :key="tab.id"
              class="whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm"
              :class="[
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:border-gray-300 dark:hover:border-gray-600'
                ]"
              @click="activeTab = tab.id"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- Tab Panels -->
      <div class="mt-4">
        <div v-show="activeTab === 'overview'" class="overflow-hidden">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">API Billing</h2>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Pay-as-you-go API usage and billing</p>
            </div>
            <button
                class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                @click="showAddFundsDialog = true"
            >
              Add Funds
            </button>
          </div>

          <div class="mt-4 bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
            <div class="flex items-baseline gap-2" v-if="wallet">
              <span class="text-3xl font-bold text-gray-900 dark:text-gray-100">${{ roundStringToTwoDecimals(wallet.balance) }}</span>
              <span class="text-sm text-gray-500 dark:text-gray-400">available balance</span>
            </div>
          </div>
        </div>

        <!-- Payment History Panel -->
        <div v-show="activeTab === 'history'" class="overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-800">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Amount</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
            </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="payment in payments" :key="payment.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                {{ formatDate(payment.date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                {{ payment.type }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                ${{ payment.amount.toFixed(2) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusClass(payment.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                      {{ payment.status }}
                    </span>
              </td>
            </tr>
            <tr v-if="payments.length === 0">
              <td colspan="4" class="px-6 py-4 text-sm text-center text-gray-500 dark:text-gray-400">
                No payment history available
              </td>
            </tr>
            </tbody>
          </table>
        </div>

        <!-- Usage Panel -->
        <div v-show="activeTab === 'usage'" class="overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700">
          <div class="p-6 text-center text-sm text-gray-500 dark:text-gray-400">
            Usage statistics coming soon
          </div>
        </div>
      </div>
    </div>

    <!-- Add Funds Dialog -->
    <TransitionRoot appear :show="showAddFundsDialog" as="template">
      <Dialog as="div" @close="showAddFundsDialog = false" class="relative z-10">
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
                <DialogTitle as="h3" class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
                  Add Funds
                </DialogTitle>

                <form @submit.prevent="handleAddFunds" class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Amount (USD)
                    </label>
                    <div class="relative">
                      <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-500 dark:text-gray-400">$</span>
                      <input
                          v-model="amount"
                          type="number"
                          min="10"
                          step="10"
                          class="pl-7 w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                          placeholder="100"
                      />
                    </div>
                    <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">Minimum amount: $10</p>
                  </div>

                  <div class="mt-6 flex justify-end gap-3">
                    <button
                        type="button"
                        class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                        @click="showAddFundsDialog = false"
                    >
                      Cancel
                    </button>
                    <button
                        type="submit"
                        class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                        :disabled="!amount || amount < 10"
                    >
                      Add Funds
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
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {usePaymentsStore} from '~/stores/payments'
import {usePayment} from '~/composables/usePayment'

const tabs = [
  {id: 'overview', name: 'Overview'},
  // {id: 'history', name: 'Payment History'},
  {id: 'usage', name: 'Usage'}
]

const activeTab = ref('overview')
const showAddFundsDialog = ref(false)
const amount = ref<number | null>(null)
const userStore = useUserStore()
const paymentsStore = usePaymentsStore()
const walletStore = useWalletStore()
const {openRazorpay} = usePayment()
const isProcessing = ref(false)

const {wallet} = storeToRefs(walletStore)

function roundStringToTwoDecimals(numStr: string): number {
  const num = parseFloat(numStr);
  if (isNaN(num)) return 0; // or throw error
  return Math.round((num + Number.EPSILON) * 100) / 100;
}

// Sample payment history data
const payments = ref([
  {
    id: 1,
    date: '2024-03-15',
    type: 'Add Funds',
    amount: 100.00,
    status: 'completed'
  },
  {
    id: 2,
    date: '2024-03-10',
    type: 'API Usage',
    amount: -25.50,
    status: 'completed'
  },
  {
    id: 3,
    date: '2024-03-01',
    type: 'Add Funds',
    amount: 50.00,
    status: 'completed'
  }
])

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'completed':
      return 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-400'
    case 'pending':
      return 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-400'
    case 'failed':
      return 'bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-400'
    default:
      return 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-400'
  }
}

const handleAddFunds = async () => {
  if (!amount.value) return

  isProcessing.value = true
  try {
    const payment = await paymentsStore.createPayment(amount.value * 100)

    if (payment) {
      openRazorpay({
        id: payment.order_id,
        key: payment.key,
        amount: payment.amount,
        currency: payment.currency,
        name: 'Add Funds to DeepCite',
        description: `Adding $${amount.value} to your account`,
        prefill: {
          name: userStore.fullName,
          email: userStore.profile?.email,
        }
      }, handlePaymentCompletion)
    }
  } catch (error) {
    console.error('Payment creation failed:', error)
  } finally {
    isProcessing.value = false
    showAddFundsDialog.value = false
    amount.value = null
  }
}

const handlePaymentCompletion = async (orderId, paymentId, signature) => {
  await paymentsStore.updatePaymentStatus(orderId, paymentId, signature)
  await walletStore.fetchWallet()
}

onMounted(() => {
  walletStore.fetchWallet()
})
</script>