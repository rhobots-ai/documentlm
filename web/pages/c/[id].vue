<template>
    <div class="min-h-[calc(100vh - 16rem)] flex flex-col">
        <div class="h-full flex-1 max-w mx-auto w-full">
            <div class="flex-1 lg:grid lg:grid-cols-7 gap-4 relative p-6">
                <!-- Chat Interface (Center) -->
                <div
                    class="lg:col-span-3 lg:mb-0"
                    v-if="conversation"
                >
                    <StudioChatInterface
                        :conversation="conversation"
                        :selected-message="selectedMessage"
                        :is-white-labeled="isWhiteLabeled"
                        @show-evidence="handleShowEvidence"
                        @update-deep-dive="handleUpdateDeepDive"
                        @show-rename-dialog="showRenameDialog = true"
                    />
                </div>

                <!-- Right Column with Tabs -->
                <div class="hidden lg:block lg:col-span-4 h-[calc(100vh-6rem)] sticky top-16">
                    <StudioDeepDive
                        v-if="!isMobile && conversation"
                        :message="selectedMessage"
                        :active-tab="activeTab"
                        :data-sources="conversation.data_sources.length != 0 ? conversation.data_sources : conversation.space.data_sources"
                    />
                </div>

                <StudioMobileDialog
                    v-if="isMobile && conversation"
                    :show="showDeepDive"
                    :message="selectedMessage || conversation?.messages?.filter(m => m.role === 'agent').at(-1)"
                    :data-sources="conversation.data_sources.length != 0 ? conversation.data_sources : conversation.space.data_sources"
                    @close="showDeepDive = false"
                />
            </div>

            <StudioRenameDialog
                :show="showRenameDialog"
                :initial-name="conversation?.name || ''"
                @close="showRenameDialog = false"
                @rename="handleRename"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import {onUnmounted, provide, ref} from 'vue'
import {useWindowSize} from '@vueuse/core'
import mitt from 'mitt'
import type {Message} from '~/types/message'

const organizationsStore = useOrganizationStore()
const conversationsStore = useConversationsStore()
const notesStore = useConversationNotesStore()
const route = useRoute()

// Get path parameters
const conversationId = computed(() => route.params.id as string)
const {currentConversation: conversation} = storeToRefs(conversationsStore)
const {isWhiteLabeled} = storeToRefs(organizationsStore)
const space = computed(() => conversation.value?.space)

const {width} = useWindowSize()
const isMobile = computed(() => width.value < 1024)

// Rename dialog
const showRenameDialog = ref(false)
const activeTab = ref<string>(null)

watch(() => conversation.value, (newConversation) => {
    if (newConversation) {
        useHead({
            title: newConversation.name || 'Untitled Conversation'
        })

        selectedMessage.value = newConversation?.messages?.filter(m => m.role === 'agent').at(-1)
    }
})

// Fetch conversation data
onMounted(() => {
    conversationsStore.fetchConversation(conversationId.value)
    notesStore.fetchNotes(conversationId.value)
})

onUnmounted(() => {
    conversationsStore.currentConversation = null;
    notesStore.notes = []
})

const emitter = mitt()
provide('emitter', emitter)

const showDeepDive = ref(false)
const selectedMessage = ref<Message | null>(null)

const handleShowEvidence = () => {
    activeTab.value = 'text'
}

const handleUpdateDeepDive = (message: Message, openDeepDive: boolean = false) => {
    selectedMessage.value = message
    activeTab.value = 'text'
    if (openDeepDive) {
        showDeepDive.value = true
    }
}

const handleRename = async (name: string) => {
    if (!conversation.value) return

    try {
        await conversationsStore.renameConversation(conversation.value.id, name)
        conversation.value.name = name
        showRenameDialog.value = false
    } catch (error) {
        console.error('Error renaming conversation:', error)
    }
}
</script>