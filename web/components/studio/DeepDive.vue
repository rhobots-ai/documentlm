<template>
  <div class="h-full flex flex-col space-y-4 overflow-hidden">
    <!-- Tools Card -->
    <div v-if="false" class="bg-white dark:bg-gray-900 backdrop-blur-sm rounded-lg border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap items-center gap-2">
        <button
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-50 dark:bg-amber-900/50 text-amber-700 dark:text-amber-400 border border-amber-200 dark:border-amber-700 hover:bg-amber-100 dark:hover:bg-amber-900/70 transition-colors text-xs font-medium"
            @click="showAddNoteSheet = true">
          <StickyNote class="h-3.5 w-3.5"/>
          Add Note
        </button>
        <button
            v-show="false"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-indigo-50 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-400 border border-indigo-200 dark:border-indigo-700 hover:bg-indigo-100 dark:hover:bg-indigo-900/70 transition-colors text-xs font-medium"
        >
          <ListCollapse class="h-3.5 w-3.5"/>
          Summarize Notes
        </button>
        <button
            v-show="false"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-purple-50 dark:bg-purple-900/50 text-purple-700 dark:text-purple-400 border border-purple-200 dark:border-purple-700 hover:bg-purple-100 dark:hover:bg-purple-900/70 transition-colors text-xs font-medium">
          <Headphones class="h-3.5 w-3.5"/>
          Audio Summary
        </button>
        <button
            v-show="false"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-50 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-700 hover:bg-emerald-100 dark:hover:bg-emerald-900/70 transition-colors text-xs font-medium">
          <Network class="h-3.5 w-3.5"/>
          Mind Map
        </button>
      </div>
    </div>

    <!-- Document Analysis Card -->
    <div
        class="bg-white dark:bg-gray-900 backdrop-blur-sm rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm h-full">
      <div class="flex border-b border-gray-200/60 dark:border-gray-700/60">
        <button
            class="px-4 py-2 text-sm font-medium transition-colors"
            :class="activeTab === 'mindmap' ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-600 dark:border-primary-400' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'"
            @click="activeTab = 'mindmap'"
        >
          Mind Map
        </button>
        <button
            class="px-4 py-2 text-sm font-medium transition-colors"
            :class="activeTab === 'text' ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-600 dark:border-primary-400' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'"
            @click="activeTab = 'text'"
        >
          Evidences
          <span
              class="ml-2 px-1.5 py-0.5 text-xs rounded-full bg-primary-100 dark:bg-primary-900/50 text-primary-600 dark:text-primary-400 transition-all duration-300 animate-in fade-in zoom-in"
          >
              {{ message?.citation?.length || 0 }}
            </span>
        </button>
        <button
            class="px-4 py-2 text-sm font-medium transition-colors"
            :class="activeTab === 'notes' ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-600 dark:border-primary-400' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'"
            @click="activeTab = 'notes'"
        >
          Notes
          <span
              class="ml-2 px-1.5 py-0.5 text-xs rounded-full bg-primary-100 dark:bg-primary-900/50 text-primary-600 dark:text-primary-400 transition-all duration-300 animate-in fade-in zoom-in"
          >
              {{ notes.length }}
            </span>
        </button>
      </div>
      <div class="p-2 h-[calc(100vh-10rem)] overflow-y-auto">
        <StudioMindMap4 v-if="activeTab === 'mindmap' && message?.mindmap" :data="message.mindmap"/>
        <StudioEvidence v-else-if="activeTab === 'text'" :citations="message?.citation" :data-sources="dataSources"/>
        <div v-else-if="activeTab === 'notes'" class="h-full">
          <div class="flex items-center justify-between">
            <h2 class="text-sm font-medium text-gray-700 dark:text-gray-300">My Notes</h2>
            <div class="flex items-center gap-2">
              <button
                  class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400 border border-primary-200 dark:border-primary-700 hover:bg-primary-100 dark:hover:bg-primary-900/70 transition-colors text-xs font-medium"
                  @click="showAddNoteSheet = true">
                <Plus class="h-3.5 w-3.5"/>
                Add Note
              </button>
            </div>
          </div>
          <div class="space-y-3 mt-2">
            <div v-if="notes.length === 0"
                 class="text-center py-12 text-gray-500 dark:text-gray-400 text-sm">
              <StickyNote class="h-8 w-8 mx-auto mb-2 text-gray-400 dark:text-gray-600"/>
              No notes yet. Create your first note by clicking on 'Add Note' above.
            </div>
            <div
                v-else
                v-for="note in notes"
                :key="note.id"
                class="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-lg border border-gray-200/60 dark:border-gray-700/60 p-3 hover:bg-white/80 dark:hover:bg-gray-900/80 transition-colors"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                    <span
                        class="text-xs font-medium px-2 py-0.5 rounded"
                        :class="getNoteTypeStyle(note.type)"
                    >
                      {{ note.type }}
                    </span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(note.created_at) }}</span>
                </div>
                <button
                    class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    @click="handleEditNote(note)"
                >
                  <Pencil class="h-3.5 w-3.5"/>
                </button>
              </div>
              <div class="text-sm text-gray-600 dark:text-gray-300 prose prose-sm max-w-none" v-html="note.content">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Note Sidesheet -->
  <StudioAddNoteSidesheet
      v-if="message"
      :show="showAddNoteSheet"
      :conversation-id="message?.conversation_id"
      @close="showAddNoteSheet = false"
  />

  <!-- Edit Note Sidesheet -->
  <StudioEditNoteSidesheet
      v-if="selectedNote"
      :show="showEditNoteSheet"
      :note="selectedNote"
      @close="handleCloseEdit"
  />
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {BookOpen, Headphones, HelpCircle, List, ListChecks, ListCollapse, Network, Pencil, Plus, StickyNote} from 'lucide-vue-next'
import type {Message} from "~/types/message";
import type {ConversationNote} from "~/types/conversation_note";
import type {DataSource} from "~/types/data_source";

const props = defineProps<{
  message?: Message | null,
  activeTab?: string,
  dataSources: DataSource[]
}>()

const notesStore = useConversationNotesStore()
const {notes, loading} = storeToRefs(notesStore)
const showAddNoteSheet = ref(false)
const showEditNoteSheet = ref(false)
const selectedNote = ref<ConversationNote | null>(null)

const activeTab = ref('text')

const noteTypes = [
  {
    name: 'Study Guide',
    icon: BookOpen
  },
  {
    name: 'Summary',
    icon: ListChecks
  },
  {
    name: 'FAQs',
    icon: HelpCircle
  },
  {
    name: 'Bullet Points',
    icon: List
  }
]

const getNoteTypeStyle = (type: string) => {
  switch (type) {
    case 'Summary':
      return 'bg-green-50 dark:bg-green-900/50 text-green-700 dark:text-green-400'
    case 'FAQs':
      return 'bg-purple-50 dark:bg-purple-900/50 text-purple-700 dark:text-purple-400'
    case 'Study Guide':
      return 'bg-blue-50 dark:bg-blue-900/50 text-blue-700 dark:text-blue-400'
    case 'Bullet Points':
      return 'bg-orange-50 dark:bg-orange-900/50 text-orange-700 dark:text-orange-400'
    case 'note':
      return 'bg-pink-50 dark:bg-pink-900/50 text-pink-700 dark:text-pink-400'
    default:
      return 'bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
  }

}

const formatDate = (timestamp: string) => {
  return new Date(timestamp).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric'
  })
}

const handleEditNote = (note: ConversationNote) => {
  selectedNote.value = note
  showEditNoteSheet.value = true
}

const handleCloseEdit = () => {
  showEditNoteSheet.value = false
  selectedNote.value = null
}

watch(() => props.message, (newMessage: Message) => {
  if (newMessage && newMessage.citation_type === 'highlight') {
    setTimeout(() => {
      document.querySelectorAll('mark').forEach(el => {
        el.classList.add(
            'bg-yellow-200',
            'outline',
            'outline-yellow-400',
            'transition-colors',
            'duration-300'
        )
      })
      activeTab.value = 'text'
    }, 100)
  }
}, {immediate: true})
</script>