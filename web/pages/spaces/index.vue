<template>
  <div class="p-6">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Spaces</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Discover and join spaces</p>
        </div>
        <button
            class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
            @click="showCreateDialog = true"
        >
          <div class="flex items-center gap-2">
            <Plus class="h-4 w-4" />
            Create Space
          </div>
        </button>
      </div>

      <!-- Search Bar -->
      <div class="relative mb-6">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-gray-500" />
        <input
            v-model="searchQuery"
            type="text"
            placeholder="Search spaces..."
            class="w-full pl-10 pr-4 py-2 rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
        />
      </div>

      <!-- Space Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
            v-for="space in filteredSpaces"
            :key="space.id"
        >
          <SpaceCard
              :space="space"
              @update:joined="updateJoinStatus(space.id, $event)"
          />
        </div>
      </div>
    </div>

    <!-- Create Space Dialog -->
    <TransitionRoot appear :show="showCreateDialog" as="template">
      <Dialog as="div" @close="showCreateDialog = false" class="relative z-10">
        <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0"
            enter-to="opacity-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100"
            leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
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
                  Create Space
                </DialogTitle>

                <form @submit.prevent="handleCreateSpace" class="space-y-4">
                  <!-- Space Name -->
                  <div>
                    <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Space Name
                    </label>
                    <input
                        v-model="form.name"
                        type="text"
                        id="name"
                        required
                        placeholder="e.g., AI Research Hub"
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                    />
                  </div>

                  <!-- Description -->
                  <div>
                    <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Description
                    </label>
                    <textarea
                        v-model="form.description"
                        id="description"
                        required
                        rows="3"
                        placeholder="Describe the purpose of your space..."
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                    ></textarea>
                  </div>

                  <!-- Space Icon -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Icon
                    </label>
                    <div class="grid grid-cols-4 gap-3">
                      <button
                          v-for="icon in icons"
                          :key="icon.name"
                          type="button"
                          class="aspect-square rounded-lg border-2 flex items-center justify-center transition-colors"
                          :class="form.icon === icon.name ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400' : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'"
                          @click="form.icon = icon.name"
                      >
                        <component :is="icon.component" class="h-6 w-6" :class="form.icon === icon.name ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'" />
                      </button>
                    </div>
                  </div>

                  <div class="flex justify-end gap-3 mt-6">
                    <button
                        type="button"
                        class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                        @click="showCreateDialog = false"
                    >
                      Cancel
                    </button>
                    <button
                        type="submit"
                        class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                        :disabled="isCreating"
                    >
                      {{ isCreating ? 'Creating...' : 'Create Space' }}
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
import { ref, computed } from 'vue'
import { Search, Microscope, Brain, Users, BookOpen, Plus, Beaker, FlaskRound as Flask, BellDot } from 'lucide-vue-next'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { useSpacesStore } from '~/stores/spaces'
import { storeToRefs } from 'pinia'

const searchQuery = ref('')
const showCreateDialog = ref(false)
const isCreating = ref(false)
const spacesStore = useSpacesStore()
const { spaces, loading } = storeToRefs(spacesStore)

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
  icon: 'Brain'
})

const handleCreateSpace = async () => {
  isCreating.value = true
  try {
    await spacesStore.createSpace(
        form.value.name,
        form.value.description,
        form.value.icon
    )

    showCreateDialog.value = false
    form.value = {
      name: '',
      description: '',
      icon: 'Brain'
    }
  } catch (error) {
    console.error('Error creating space:', error)
  } finally {
    isCreating.value = false
  }
}

const filteredSpaces = computed(() => {
  const query = searchQuery.value.toLowerCase()
  return spaces.value.filter(space =>
      space.name.toLowerCase().includes(query) ||
      space.description.toLowerCase().includes(query)
  )
})

const updateJoinStatus = async (spaceId: string, joined: boolean) => {
  try {
    if (joined) {
      await spacesStore.joinSpace(spaceId)
    } else {
      await spacesStore.leaveSpace(spaceId)
    }
  } catch (error) {
    console.error('Error updating join status:', error)
  }
}

onMounted(() => {
  spacesStore.fetchSpaces()
})
</script>