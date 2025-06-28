<template>
  <div class="p-6">
    <div class="max-w-3xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Create Space</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Set up a new collaborative research space</p>
      </div>

      <form @submit.prevent="createSpace" class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
        <!-- Space Name -->
        <div class="mb-6">
          <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Space Name</label>
          <input
            v-model="form.name"
            type="text"
            id="name"
            placeholder="e.g., AI Research Hub"
            class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
            required
          />
        </div>

        <!-- Space Description -->
        <div class="mb-6">
          <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
          <textarea
            v-model="form.description"
            id="description"
            rows="3"
            placeholder="Describe the purpose of your space..."
            class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
            required
          ></textarea>
        </div>

        <!-- Space Icon -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Icon</label>
          <div class="grid grid-cols-4 gap-3">
            <button
              v-for="icon in icons"
              :key="icon.name"
              type="button"
              class="aspect-square rounded-lg border-2 flex items-center justify-center transition-colors"
              :class="form.icon === icon.component ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'"
              @click="form.icon = icon.component"
            >
              <component :is="icon.component" class="h-6 w-6" :class="form.icon === icon.component ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'" />
            </button>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="flex items-center justify-end gap-3">
          <NuxtLink
            to="/spaces"
            class="px-4 py-2 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
          >
            Cancel
          </NuxtLink>
          <button
            type="submit"
            class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
          >
            Create Space
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Brain, Microscope, BookOpen, Users, Beaker, FlaskRound as Flask, BellDot } from 'lucide-vue-next'

const router = useRouter()

const icons = [
  { name: 'Brain', component: Brain },
  { name: 'Microscope', component: Microscope },
  { name: 'Book', component: BookOpen },
  { name: 'Users', component: Users },
  { name: 'Beaker', component: Beaker },
  { name: 'Flask', component: Flask },
  { name: 'BellDot', component: BellDot }
]

const form = ref({
  name: '',
  description: '',
  icon: Brain
})

const createSpace = () => {
  // TODO: Implement space creation logic
  console.log('Creating space:', form.value)
  router.push('/spaces')
}
</script>