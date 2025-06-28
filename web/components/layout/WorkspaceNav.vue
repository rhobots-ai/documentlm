<template>
  <!-- Delete Confirmation Dialog -->
  <TransitionRoot appear :show="showDeleteDialog" as="template">
    <Dialog as="div" @close="showDeleteDialog = false" class="relative z-[60]">
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
                Delete "{{ itemToDelete?.name }}"?
              </DialogTitle>

              <div class="mt-2">
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  Are you sure you want to delete this tag? This action cannot be undone.
                </p>

                <!-- Affected Spaces -->
                <div v-if="affectedSpaces.length > 0" class="mt-4">
                  <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    The following spaces will be untagged:
                  </h4>
                  <ul class="space-y-2">
                    <li
                        v-for="space in affectedSpaces"
                        :key="space.id"
                        class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400"
                    >
                      <component :is="space.icon" class="h-4 w-4 text-gray-400 dark:text-gray-500"/>
                      {{ space.name }}
                    </li>
                  </ul>
                </div>
              </div>

              <div class="mt-6 flex justify-end gap-3">
                <button
                    class="px-3 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    @click="showDeleteDialog = false"
                >
                  Cancel
                </button>
                <button
                    class="px-3 py-2 rounded-lg bg-red-600 text-white text-sm font-medium hover:bg-red-700 transition-colors"
                    @click="confirmDelete"
                >
                  Delete
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>

  <template v-for="section in workspaceItems" :key="section.id">
    <div class="mt-1 px-4">
      <LayoutWorkspaceTreeItem
          :item="section"
          :selected-item="isSelected ? selectedItem : null"
          :is-edit-mode="isEditMode"
          :is-root="section.id === 'root'"
          :items="workspaceItems"
          @select="handleSelect"
          @add="handleAdd"
          @delete="handleDelete"
          @rename="handleRename"
          @toggle-edit="handleEditToggle"
      />
    </div>
  </template>
</template>

<script setup lang="ts">
  import {nextTick, ref} from 'vue'
  import {BookOpen, Brain, Microscope} from 'lucide-vue-next'
  import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
  import type {WorkspaceItem} from "~/types/workspance_item";
  import {storeToRefs} from "pinia";
  import {useUserStore} from "~/stores/user";

  const props = defineProps<{
    isWhiteLabeled?: boolean
    isSelected: boolean
  }>()

  const emit = defineEmits<{
    (e: 'close'): void
    (e: 'navigate'): void
    (e: 'update:items', items: WorkspaceItem[]): void
  }>()

  const tagsStore = useTagsStore()
  const userStore = useUserStore()

  const {tags, loading: tagsLoading} = storeToRefs(tagsStore)
  const {isLoggedIn} = storeToRefs(userStore)

  // Root workspace item that will contain tags
  const workspaceItems = ref<WorkspaceItem[]>([])

  // Convert tags to workspace items
  const convertTagsToWorkspaceItems = () => {
    // Create a map to store items by ID for quick lookup
    const itemsMap = new Map<string, WorkspaceItem>()

    workspaceItems.value = [
      {
        id: 'root',
        name: 'Workspace',
        expanded: true,
        items: []
      }
    ]

    // Add root item to map
    itemsMap.set('root', workspaceItems.value[0])

    // First pass: create all items
    tags.value.forEach(tag => {
      const item: WorkspaceItem = {
        id: tag.id,
        name: tag.name,
        path: `/workspace/${tag.name.toLowerCase().replace(/\s+/g, '-')}`,
        parentId: tag.parent_id || 'root',
        expanded: false,
        items: []
      }

      itemsMap.set(tag.id, item)
    })

    // Second pass: build the hierarchy
    tags.value.forEach(tag => {
      const item = itemsMap.get(tag.id)
      const parentItem = itemsMap.get(tag.parent_id || 'root')

      if (parentItem && item) {
        if (!parentItem.items) {
          parentItem.items = []
        }
        parentItem.items.push(item)
      }
    })

    // Update the root item's children
    workspaceItems.value[0].items = itemsMap.get('root')?.items || []
  }

  watch(() => props.isWhiteLabeled, (newIsWhiteLabeled) => {
    if (newIsWhiteLabeled) {
      tagsStore.fetchTags()
    }
  })

  // Fetch tags when component mounts
  onMounted(async () => {
    if (isLoggedIn.value || props.isWhiteLabeled) {
      await tagsStore.fetchTags()
    }
  })

  // Watch for changes in tags
  watch(() => tags.value, () => {
    convertTagsToWorkspaceItems()
  }, {deep: true})

  // Sample data for affected spaces - replace with actual data in production
  const sampleSpaces = [
    {
      id: 1,
      name: 'AI Research Hub',
      icon: Brain,
      tags: ['research', 'technical'],
      data_sources: []
    },
    {
      id: 2,
      name: 'Medical Studies',
      icon: Microscope,
      tags: ['research'],
      data_sources: []
    },
    {
      id: 3,
      name: 'Academic Papers',
      icon: BookOpen,
      tags: ['research', 'technical'],
      data_sources: []
    }
  ]

  const showDeleteDialog = ref(false)
  const itemToDelete = ref<WorkspaceItem | null>(null)
  const affectedSpaces = ref<any[]>([])
  const isEditMode = ref(false)

  const selectedItem = ref<WorkspaceItem | null>(null)

  const handleSelect = (item: WorkspaceItem) => {
    selectedItem.value = item
    if (!item.items?.length) {
      emit('navigate')
    }
  }

  const handleAdd = (parentId: string) => {
    // Generate a random color for the new tag
    const colors = ['blue', 'green', 'purple', 'amber', 'rose', 'indigo'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];

    // Create a new tag via the API
    tagsStore.createTag('New Tag', randomColor, parentId === 'root' ? null : parentId)
        .then((newTag) => {
          // Refresh tags after creation
          tagsStore.fetchTags();
        })
        .catch((error) => {
          console.error('Error creating tag:', error);
        });
  }

  const handleDelete = (item: WorkspaceItem) => {
    itemToDelete.value = item
    // Get all child tags including the current one
    const allTags = getAllChildTags(item)

    // Find spaces that have any of these tags
    affectedSpaces.value = sampleSpaces.filter(space =>
        space.tags.some(tag => allTags.includes(tag.toLowerCase()))
    )
    showDeleteDialog.value = true
  }

  const handleRename = (item: { id: string, name: string }) => {
    // Find the tag in the store
    const tag = tags.value.find(t => t.id === item.id);
    if (tag) {
      // Update the tag via API
      tagsStore.updateTag(item.id, {name: item.name, color: tag.color, parent_id: tag.parent_id})
          .then(() => {
            // Refresh tags after update
            tagsStore.fetchTags();
          })
          .catch((error) => {
            console.error('Error updating tag:', error);
          });
    }
  }

  const editInput = ref<HTMLInputElement | null>(null)

  const startEdit = async (item: WorkspaceItem) => {
    item.isEditing = true
    item.editName = item.name
    await nextTick()
    editInput.value?.focus()
  }

  const saveEdit = (item: WorkspaceItem) => {
    if (item.isEditing && item.editName && item.editName !== item.name) {
      item.name = item.editName
    }
    item.isEditing = false
    item.editName = undefined
  }

  const deleteItem = (item: WorkspaceItem) => {
    itemToDelete.value = item
    // Get all child tags including the current one
    const allTags = getAllChildTags(item)

    // Find spaces that have any of these tags
    affectedSpaces.value = sampleSpaces.filter(space =>
        space.tags.some(tag => allTags.includes(tag.toLowerCase()))
    )
    showDeleteDialog.value = true
  }

  const getAllChildTags = (item: WorkspaceItem): string[] => {
    const tags: string[] = [item.name.toLowerCase()]

    if (item.items) {
      item.items.forEach(child => {
        tags.push(...getAllChildTags(child))
      })
    }

    return tags
  }

  const confirmDelete = () => {
    if (!itemToDelete.value) return

    // Delete the tag via API
    tagsStore.deleteTag(itemToDelete.value.id)
        .then(() => {
          // Refresh tags after deletion
          tagsStore.fetchTags();
        })
        .catch((error) => {
          console.error('Error deleting tag:', error);
        });

    showDeleteDialog.value = false
    itemToDelete.value = null
    affectedSpaces.value = []
  }

  const handleEditToggle = () => {
    if (isEditMode.value) {
      // Save all currently editing items before disabling edit mode
      const saveAllEdits = (items: WorkspaceItem[]) => {
        items.forEach(item => {
          if (item.isEditing) {
            saveEdit(item)
          }
          if (item.items) {
            saveAllEdits(item.items)
          }
        })
      }
      saveAllEdits(workspaceItems.value)
    }
    isEditMode.value = !isEditMode.value
  }
</script>