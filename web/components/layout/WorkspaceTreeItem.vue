<template>
  <div class="group">
    <div class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors mt-1" :class="{ 'pl-4 pr-3 py-2': !isRoot }">
      <button
          class="flex-1 flex items-center gap-2 rounded-lg text-sm transition-colors"
          :class="buttonClasses"
          @click="handleClick(item, $event)"
      >
        <span v-if="!item.isEditing" class="flex-1 text-left" :class="{'text-primary-500' : item.id == selectedItem?.id}">{{ item.name }}</span>
        <input
            v-else
            v-model="item.editName"
            type="text"
            class="flex-1 bg-transparent border-none focus:ring-0 p-0 text-sm"
            @keyup.enter="saveEdit"
            @blur="saveEdit"
            ref="editInput"
        />
        <ChevronRight
            v-if="hasChildren"
            class="h-4 w-4 transition-transform"
            :class="{ 'rotate-90': item.expanded, 'h-3 w-3': !isRoot }"
        />
      </button>

      <!-- Root Actions -->
      <div v-if="false && isRoot" class="flex items-center gap-1">
        <button
            v-if="isEditMode"
            class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 dark:text-gray-500"
            @click="$emit('add', item.id)"
        >
          <Plus class="h-3.5 w-3.5" />
        </button>
        <button
            v-if="isRoot"
            class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 dark:text-gray-500"
            @click="$emit('toggle-edit')"
        >
          <component
              :is="isEditMode ? Save : Pencil"
              class="h-3.5 w-3.5"
              :class="{ 'text-primary-600 dark:text-primary-400': isEditMode }"
          />
        </button>
      </div>

      <!-- Item Actions -->
      <div v-else-if="isEditMode" class="flex items-center gap-1">
        <button
            class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 dark:text-gray-500"
            @click="startEdit"
        >
          <Pencil class="h-3 w-3" />
        </button>
        <button
            class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 dark:text-gray-500"
            @click="$emit('add', item.id)"
        >
          <Plus class="h-3 w-3" />
        </button>
        <button
            class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 dark:text-gray-500"
            @click="$emit('delete', item)"
        >
          <Trash class="h-3 w-3" />
        </button>
      </div>
    </div>

    <!-- Children -->
    <div
        v-if="hasChildren && item.expanded"
        class="ml-4 mt-1 space-y-1 border-l border-gray-200 dark:border-gray-700"
    >
      <LayoutWorkspaceTreeItem
          v-for="child in item.items"
          :key="child.id"
          :item="child"
          :selected-item="selectedItem"
          :items="props.items"
          :is-edit-mode="isEditMode"
          :is-sub-item="hasChildren"
          @select="$emit('select', $event)"
          @add="$emit('add', $event)"
          @delete="$emit('delete', $event)"
          @rename="$emit('rename', $event)"
          @toggle-edit="$emit('toggle-edit')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, ref, nextTick } from 'vue'
  import { ChevronRight, Pencil, Plus, Trash, Save } from 'lucide-vue-next'
  import type {WorkspaceItem} from "~/types/workspance_item";

  const props = defineProps<{
    item: WorkspaceItem
    selectedItem: WorkspaceItem | null
    items: WorkspaceItem[]
    isEditMode: boolean
    isRoot?: boolean
    isSubItem?: boolean
  }>()

  const emit = defineEmits<{
    (e: 'add', id: string): void
    (e: 'delete', item: WorkspaceItem): void
    (e: 'rename', item: { id: string; name: string }): void
    (e: 'toggle-edit'): void
    (e: 'select', item: WorkspaceItem): void
  }>()

  const editInput = ref<HTMLInputElement | null>(null)
  const hasChildren = computed(() => (props.item.items?.length || 0) > 0)

  const buttonClasses = computed(() => {
    if (props.isRoot) {
      return props.isEditMode
          ? 'text-primary-600 dark:text-primary-400'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'
    }
    return 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
  })

  const startEdit = async () => {
    props.item.isEditing = true
    props.item.editName = props.item.name
    await nextTick()
    editInput.value?.focus()
  }

  const saveEdit = () => {
    if (props.item.isEditing && props.item.editName && props.item.editName !== props.item.name) {
      emit('rename', { id: props.item.id, name: props.item.editName })
    }
    props.item.isEditing = false
    props.item.editName = undefined
  }

  const findParentItem = (parentId?: string): WorkspaceItem | undefined => {
    if (!parentId) return undefined

    const searchInItems = (items: WorkspaceItem[]): WorkspaceItem | undefined => {
      for (const item of items) {
        if (item.id === parentId) return item
        if (item.items) {
          const found = searchInItems(item.items)
          if (found) return found
        }
      }
      return undefined
    }

    return searchInItems(props.items)
  }

  const handleClick = (item: WorkspaceItem, event?: MouseEvent) => {
    emit('select', item)
    const getItemPath = (currentItem: WorkspaceItem): string[] => {
      const path = [currentItem.id.toLowerCase().replace(/\s+/g, '-')]
      let parent = findParentItem(currentItem.parentId)
      while (parent) {
        path.unshift(parent.id.toLowerCase().replace(/\s+/g, '-'))
        parent = findParentItem(parent.parentId)
      }
      return path
    }

    // Handle navigation
    const pathSegments = getItemPath(item)
    const path = `/workspace/${pathSegments.join('/')}`
    navigateTo(path)

    // Handle expansion for parent nodes
    if (hasChildren.value && !props.isEditMode) {
      item.expanded = !item.expanded
    }
  }
</script>