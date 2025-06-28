<template>
  <div class="p-6">
    <div v-if="currentTag" class="max-w-7xl mx-auto space-y-6">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-2">
          <span>Workspace</span>
          <ChevronRight class="h-4 w-4"/>
          <template v-for="(segment, index) in pathSegments" :key="index">
            <span>{{ segment === 'root' ? 'root': getTagName(segment) }}</span>
            <ChevronRight v-if="index < pathSegments.length - 1" class="h-4 w-4"/>
          </template>
        </div>
<!--        <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">{{ currentTag.name }}</h1>-->
<!--        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Spaces tagged with "{{ currentTag.name }}"</p>-->
        <button
            v-if="!isWhiteLabeled && taggedSpaces.length > 0"
            @click="showTagSpacesDialog = true"
            class="mt-6 px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors inline-flex items-center gap-2"
        >
          <Tags class="h-4 w-4" />
          Tag Spaces
        </button>
      </div>


      <!-- Space Grid (when spaces are tagged) -->
      <div v-if="taggedSpaces.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="space in taggedSpaces" :key="space.id">
          <SpaceCard :space="space" @update:joined="updateJoinStatus(space.id, $event)"/>
        </div>
      </div>

      <!-- Empty State with Action -->
      <div v-if="taggedSpaces.length === 0" class="text-center py-12">
        <FolderOpen class="h-12 w-12 mx-auto text-gray-400 dark:text-gray-600"/>
        <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">No spaces found</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">No spaces are currently tagged with "{{ currentTag.name }}"</p>
        <button
            v-if="!isWhiteLabeled"
            @click="showTagSpacesDialog = true"
            class="mt-6 px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors inline-flex items-center gap-2"
        >
          <Tags class="h-4 w-4" />
          Tag Spaces
        </button>
      </div>

      <!-- Tag Spaces Dialog -->
      <TransitionRoot appear :show="showTagSpacesDialog" as="template">
        <Dialog as="div" @close="showTagSpacesDialog = false" class="relative z-10">
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
                    Tag Spaces with "{{ currentTag.name }}"
                  </DialogTitle>

                  <div class="mt-4 mb-6">
                    <div v-if="loading" class="flex justify-center py-8">
                      <Loader2 class="h-8 w-8 text-primary-600 dark:text-primary-400 animate-spin" />
                    </div>
                    <div v-else-if="availableSpaces.length === 0" class="text-center py-8">
                      <FolderOpen class="h-10 w-10 mx-auto text-gray-400 dark:text-gray-600 mb-2" />
                      <p class="text-gray-600 dark:text-gray-300">No spaces available to tag</p>
                    </div>
                    <div v-else class="space-y-3 max-h-80 overflow-y-auto pr-2">
                      <div
                          v-for="space in availableSpaces"
                          :key="space.id"
                          class="flex items-center p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                      >
                        <div class="flex-1 flex items-center gap-3">
                          <div class="h-10 w-10 rounded-lg bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
                            <component :is="getSpaceIconComponent(space.icon)" class="h-5 w-5 text-primary-600 dark:text-primary-400"/>
                          </div>
                          <div>
                            <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ space.name }}</h4>
                            <p class="text-xs text-gray-500 dark:text-gray-400 line-clamp-1">{{ space.description }}</p>
                          </div>
                        </div>
                        <div>
                          <input
                              type="checkbox"
                              :id="`space-${space.id}`"
                              v-model="selectedSpaces"
                              :value="space.id"
                              class="h-4 w-4 rounded border-gray-300 dark:border-gray-600 text-primary-600 dark:text-primary-400 focus:ring-primary-500"
                          />
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="flex justify-end gap-3">
                    <button
                        type="button"
                        class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                        @click="showTagSpacesDialog = false"
                    >
                      Cancel
                    </button>
                    <button
                        type="button"
                        class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors flex items-center gap-2"
                        :disabled="selectedSpaces.length === 0 || isUpdating"
                        @click="updateTaggedSpaces"
                    >
                      <Loader2 v-if="isUpdating" class="h-4 w-4 animate-spin" />
                      <span>{{ isUpdating ? 'Updating...' : 'Save' }}</span>
                    </button>
                  </div>
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
import {computed, ref} from 'vue'
import {ChevronRight, FolderOpen, Tags, Loader2} from 'lucide-vue-next'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {getSpaceIconComponent} from "~/utils/icons";

const route = useRoute()

const tagsStore = useTagsStore()
const spacesStore = useSpacesStore()
const organizationStore = useOrganizationStore()
const {tags} = storeToRefs(tagsStore)
const {spaces} = storeToRefs(spacesStore)
const {isWhiteLabeled} = storeToRefs(organizationStore)

const showTagSpacesDialog = ref(false)
const selectedSpaces = ref<string[]>([])
const isUpdating = ref(false)
const loading = ref(false)

const allTags = computed(() => {
  return tags.value
})

const pathSegments = computed(() => {
  const path = route.params.path
  return Array.isArray(path) ? path : [path]
})

const currentTag = computed(() => {
  const currentTagId = pathSegments.value[pathSegments.value.length - 1]
  return allTags.value.find(t => t.id === currentTagId)
})

const getTagName = (tagId: string) => {
  return allTags.value.find(t => t.id === tagId)?.name
}

// Spaces that are already tagged with the current tag
const taggedSpaces = computed(() => {
  return currentTag.value?.spaces || []
})

// Spaces that are not yet tagged with the current tag
const availableSpaces = computed(() => {
  const taggedSpaceIds = taggedSpaces.value.map(space => space.id)
  return spaces.value.filter(space => !taggedSpaceIds.includes(space.id))
})

// Initialize selected spaces when dialog opens
watch(showTagSpacesDialog, (isOpen) => {
  if (isOpen) {
    loading.value = true
    spacesStore.fetchSpaces().then(() => {
      loading.value = false
    })
    selectedSpaces.value = []
  }
})

// Update tag with selected spaces
const updateTaggedSpaces = async () => {
  if (!currentTag.value || selectedSpaces.value.length === 0) return

  isUpdating.value = true
  try {
    await tagsStore.updateTag(currentTag.value.id, {
      spaces_to_tag: selectedSpaces.value,
      spaces_to_untag: []
    })

    // Refresh the current tag to update the UI
    await tagsStore.fetchTag(currentTag.value.id)

    showTagSpacesDialog.value = false
  } catch (error) {
    console.error('Error updating tagged spaces:', error)
  } finally {
    isUpdating.value = false
  }
}

const updateJoinStatus = (spaceId: string, joined: boolean) => {
  // Implementation for joining/leaving spaces
}

onMounted(() => {
  // Fetch tags if not already loaded
  if (tags.value.length === 0) {
    tagsStore.fetchTags()
  }
})
</script>