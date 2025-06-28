<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" @close="handleClose" class="relative z-50">
      <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <div class="fixed inset-y-0 right-0 max-w-full flex">
        <TransitionChild
            as="template"
            enter="transform transition ease-in-out duration-300"
            enter-from="translate-x-full"
            enter-to="translate-x-0"
            leave="transform transition ease-in-out duration-200"
            leave-from="translate-x-0"
            leave-to="translate-x-full"
        >
          <DialogPanel class="w-screen max-w-md">
            <div class="h-full flex flex-col bg-white dark:bg-gray-900 shadow-xl">
              <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <div class="flex items-center justify-between">
                  <DialogTitle as="h3" class="text-lg font-medium text-gray-900 dark:text-gray-100">
                    Add Note
                  </DialogTitle>
                  <button
                      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                      @click="handleClose"
                  >
                    <X class="h-5 w-5 text-gray-500 dark:text-gray-400" />
                  </button>
                </div>
              </div>

              <div class="flex-1 px-6 py-4 overflow-y-auto">
                <form @submit.prevent="handleSubmit" class="space-y-4">
                  <!-- Note Type -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Note Type
                    </label>
                    <input
                        type="text"
                        v-model="form.type"
                        maxlength="50"
                        placeholder="Enter note type..."
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                        readonly="readonly"
                        required
                    />
                  </div>

                  <!-- Note Content -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Content
                    </label>
                    <div class="border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden">
                      <!-- Editor Toolbar -->
                      <div class="flex items-center gap-1 p-2 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
                        <button
                            v-for="item in editorButtons"
                            :key="item.command"
                            type="button"
                            class="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                            :class="{ 'bg-gray-200 dark:bg-gray-700': editor?.isActive(item.command) }"
                            @click="item.action"
                        >
                          <component :is="item.icon" class="h-4 w-4 text-gray-600 dark:text-gray-300" />
                        </button>
                      </div>

                      <!-- Editor Content -->
                      <EditorContent
                          :editor="editor"
                          class="prose prose-sm max-w-none p-4 h-[calc(100vh-22rem)] text-black dark:text-white focus:outline-none overflow-y-scroll"
                      />
                    </div>
                  </div>
                </form>
              </div>

              <div class="flex justify-end gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700">
                <button
                    class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    @click="handleClose"
                >
                  Cancel
                </button>
                <button
                    class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                    :disabled="isSubmitting"
                    @click="handleSubmit"
                >
                  {{ isSubmitting ? 'Saving...' : 'Save Note' }}
                </button>
              </div>
            </div>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { X, Bold, Italic, List, ListOrdered } from 'lucide-vue-next'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { useConversationNotesStore } from '~/stores/conversation_notes'

const props = defineProps<{
  show: boolean
  conversationId: string
  initialContent?: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const notesStore = useConversationNotesStore()
const isSubmitting = ref(false)

const editor = useEditor({
  extensions: [
    StarterKit,
  ],
  content: props.initialContent || '',
  editorProps: {
    attributes: {
      class: 'prose prose-sm max-w-none focus:outline-none'
    }
  }
})

// Watch for changes in initialContent prop
watch(() => props.initialContent, (newContent) => {
  if (newContent && editor.value) {
    editor.value.commands.setContent(newContent)
  }
})

const editorButtons = [
  {
    icon: Bold,
    command: 'bold',
    action: () => editor.value?.chain().focus().toggleBold().run()
  },
  {
    icon: Italic,
    command: 'italic',
    action: () => editor.value?.chain().focus().toggleItalic().run()
  },
  {
    icon: List,
    command: 'bulletList',
    action: () => editor.value?.chain().focus().toggleBulletList().run()
  },
  {
    icon: ListOrdered,
    command: 'orderedList',
    action: () => editor.value?.chain().focus().toggleOrderedList().run()
  }
]

const form = ref({
  type: 'note',
  content: ''
})

const handleClose = () => {
  form.value = {
    type: 'note',
    content: ''
  }
  editor.value?.commands.setContent('')
  emit('close')
}

const handleSubmit = async () => {
  const content = editor.value?.getHTML() || ''
  if (!form.value.type.trim() || !content.trim()) return

  isSubmitting.value = true
  try {
    await notesStore.createNote(
        props.conversationId,
        content,
        form.value.type
    )
    handleClose()
  } catch (error) {
    console.error('Error creating note:', error)
  } finally {
    isSubmitting.value = false
  }
}

onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy()
  }
})
</script>