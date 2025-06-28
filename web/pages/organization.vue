<template>
  <div class="p-6">
    <div class="max-w-4xl mx-auto">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Organization</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Manage your team members and invitations</p>
        </div>
        <button
            v-if="activeOrganization"
            class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors flex items-center gap-2"
            @click="showSettingsDialog = true"
        >
          <Settings class="h-4 w-4"/>
          Settings
        </button>
      </div>

      <!-- Organization Section -->
      <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm mb-6">
        <div class="p-6">
          <div v-if="activeOrganization">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="m-0 font-medium text-gray-900 dark:text-gray-100">{{ activeOrganization.name }}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ activeOrganization.slug }}.{{ config.public.appBaseUrl }}</p>
              </div>
            </div>
          </div>

          <div v-else>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">Create an organization to access advanced features like API keys and team
              collaboration.</p>
            <button
                class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                @click="showCreateOrgDialog = true"
                :disabled="isCreatingOrg"
            >
              {{ isCreatingOrg ? 'Creating...' : 'Create Organization' }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="activeOrganization" class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
        <div class="p-6">
          <!-- Organization Info -->
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="m-0 text-lg font-medium text-gray-900 dark:text-gray-100">Members</h2>
            </div>
            <button
                v-if="false"
                class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                @click="showInviteDialog = true"
            >
              <div class="flex items-center gap-2">
                <UserPlus class="h-4 w-4"/>
                Invite Member
              </div>
            </button>
          </div>

          <!-- Members List -->
          <div class="divide-y divide-gray-200 dark:divide-gray-700">
            <div v-if="members" v-for="member in members" :key="member.userId" class="py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 rounded-full bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
                    <img
                        v-if="member.user.image"
                        :src="member.user.image"
                        :alt="member.user.name"
                        class="h-full w-full object-cover rounded-full"
                    />
                    <User v-else class="h-5 w-5 text-primary-600 dark:text-primary-400"/>
                  </div>
                  <div>
                    <div class="font-medium text-gray-900 dark:text-gray-100">
                      {{ member.user.name }}
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ member.user.email }}</div>
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <div class="px-2.5 py-1 rounded-full text-xs font-medium" :class="getRoleClass(member.role)">
                    {{ member.role }}
                  </div>
                  <button
                      v-if="canRemoveMember(member)"
                      class="p-2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
                      @click="confirmRemoveMember(member)"
                  >
                    <Trash2 class="h-4 w-4"/>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Pending Invitations -->
          <div v-if="pendingInvitations.length > 0" class="mt-8">
            <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-4">Pending Invitations</h3>
            <div class="divide-y divide-gray-200 dark:divide-gray-700">
              <div v-for="invitation in pendingInvitations" :key="invitation.id" class="py-4">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="font-medium text-gray-900 dark:text-gray-100">{{ invitation.email }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">Invited {{ formatDate(invitation.createdAt) }}</div>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="px-2.5 py-1 rounded-full bg-amber-50 dark:bg-amber-900/50 text-amber-700 dark:text-amber-400 text-xs font-medium">
                      Pending
                    </div>
                    <button
                        class="p-2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
                        @click="revokeInvitation(invitation.id)"
                    >
                      <X class="h-4 w-4"/>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Settings Dialog -->
    <OrganizationSettingsDialog
        v-if="organizationConfig"
        :show="showSettingsDialog"
        :initial-config="organizationConfig"
        @close="showSettingsDialog = false"
        @update="handleUpdateConfig"
    />

    <!-- Create Organization Dialog -->
    <TransitionRoot appear :show="showCreateOrgDialog" as="template">
      <Dialog as="div" @close="showCreateOrgDialog = false" class="relative z-10">
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
                  Create Organization
                </DialogTitle>

                <form @submit.prevent="handleCreateOrg" class="space-y-4">
                  <div>
                    <label for="orgName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Organization Name
                    </label>
                    <input
                        id="orgName"
                        v-model="orgForm.name"
                        type="text"
                        required
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                    />
                  </div>

                  <div>
                    <label for="orgSlug" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Organization URL
                    </label>
                    <input
                        id="orgSlug"
                        v-model="orgForm.slug"
                        type="text"
                        required
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                    />
                  </div>

                  <div class="flex justify-end gap-3 mt-6">
                    <button
                        type="button"
                        class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                        @click="showCreateOrgDialog = false"
                    >
                      Cancel
                    </button>
                    <button
                        type="submit"
                        class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                    >
                      Create
                    </button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Invite Member Dialog -->
    <TransitionRoot appear :show="showInviteDialog" as="template">
      <Dialog as="div" @close="showInviteDialog = false" class="relative z-10">
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
                  Invite Team Member
                </DialogTitle>

                <form @submit.prevent="handleInvite" class="space-y-4">
                  <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Email Address
                    </label>
                    <input
                        id="email"
                        v-model="inviteForm.email"
                        type="email"
                        required
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                    />
                  </div>

                  <div>
                    <label for="role" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Role
                    </label>
                    <select
                        id="role"
                        v-model="inviteForm.role"
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                    >
                      <option value="member">Member</option>
                      <option value="admin">Admin</option>
                    </select>
                  </div>

                  <div class="flex justify-end gap-3 mt-6">
                    <button
                        type="button"
                        class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                        @click="showInviteDialog = false"
                    >
                      Cancel
                    </button>
                    <button
                        type="submit"
                        class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
                        :disabled="isInviting"
                    >
                      {{ isInviting ? 'Sending...' : 'Send Invitation' }}
                    </button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Remove Member Dialog -->
    <TransitionRoot appear :show="showRemoveDialog" as="template">
      <Dialog as="div" @close="showRemoveDialog = false" class="relative z-10">
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
                  Remove Team Member
                </DialogTitle>

                <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
                  Are you sure you want to remove {{ selectedMember?.name }} from the team? This action cannot be undone.
                </p>

                <div class="flex justify-end gap-3">
                  <button
                      class="px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                      @click="showRemoveDialog = false"
                  >
                    Cancel
                  </button>
                  <button
                      class="px-4 py-2 rounded-lg bg-red-600 text-white text-sm font-medium hover:bg-red-700 transition-colors"
                      @click="removeMember"
                  >
                    Remove
                  </button>
                </div>
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
import {Settings, Trash2, User, UserPlus, X} from 'lucide-vue-next'
import type {OrganizationConfiguration} from "~/types/organization";

const config = useRuntimeConfig()

const userStore = useUserStore()
const {organization, useActiveOrganization} = useAuthClient()

const activeOrganization = ref<any>(null)
const activeMember = ref<any>(null)
const members = ref<any[]>([])
const pendingInvitations = ref<any[]>([])

const showCreateOrgDialog = ref(false)
const isCreatingOrg = ref(false)

const showInviteDialog = ref(false)
const showRemoveDialog = ref(false)
const isInviting = ref(false)
const showSettingsDialog = ref(false)
const selectedMember = ref<any>(null)

const orgForm = ref({
  name: '',
  slug: ''
})

const inviteForm = ref({
  email: '',
  role: 'member'
})

// Organization configuration
const organizationConfig = ref<OrganizationConfiguration | null>(null)

// Load organization data
onMounted(async () => {
  let activeOrganizationRef = useActiveOrganization.get()
  const organizationInterval = setInterval(async () => {
    if (!activeOrganizationRef.isPending) {
      clearInterval(organizationInterval)

      activeMember.value = await organization.getActiveMember()

      activeOrganization.value = activeOrganizationRef.data
      organizationConfig.value = JSON.parse(activeOrganization.value?.metadata || '{}')
      members.value = activeOrganizationRef.data?.members || []
      pendingInvitations.value = activeOrganizationRef.data?.invitations || []
    }
    activeOrganizationRef = useActiveOrganization.get()
  }, 50)
})

const handleUpdateConfig = async (newConfig: OrganizationConfiguration) => {
  showSettingsDialog.value = false
  // In a real application, you would save this to the server
  await organization.update({
    data: {
      metadata: newConfig,
    },
    organizationId: activeOrganization.value.id
  })
}

const handleInvite = async () => {
  if (!activeOrganization.value) return

  isInviting.value = true
  try {
    await activeOrganization.value.inviteMember({
      emailAddress: inviteForm.value.email,
      role: inviteForm.value.role
    })

    showInviteDialog.value = false
    inviteForm.value = {
      email: '',
      role: 'basic_member'
    }
  } catch (error) {
    console.error('Error inviting member:', error)
  } finally {
    isInviting.value = false
  }
}

const confirmRemoveMember = (member: any) => {
  selectedMember.value = member
  showRemoveDialog.value = true
}

const removeMember = async () => {
  if (!selectedMember.value) return

  try {
    await organization.removeMember({
      memberIdOrEmail: selectedMember.value.id,
      organizationId: selectedMember.value.organizationId
    })
    showRemoveDialog.value = false
    selectedMember.value = null
  } catch (error) {
    console.error('Error removing member:', error)
  }
}

const revokeInvitation = async (invitationId: string) => {
  if (!activeOrganization.value) return

  try {
    const invitation = pendingInvitations.value.find(inv => inv.id === invitationId)
    if (invitation) {
      await invitation.revoke()
    }
  } catch (error) {
    console.error('Error revoking invitation:', error)
  }
}

const canRemoveMember = (member: any) => {
  return activeMember.value.role === 'owner' && (member.role !== 'owner' || members.value.filter(m => m.role === 'owner').length > 1)
}

const getRoleClass = (role: string) => {
  switch (role) {
    case 'owner':
      return 'bg-purple-50 dark:bg-purple-900/50 text-purple-700 dark:text-purple-400'
    default:
      return 'bg-blue-50 dark:bg-blue-900/50 text-blue-700 dark:text-blue-400'
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const handleCreateOrg = async () => {
  if (activeOrganization.value) {
    showCreateOrgDialog.value = false
    return
  }

  isCreatingOrg.value = true
  try {
    // TODO: create org
    await organization.create({
      name: orgForm.value.name,
      slug: orgForm.value.slug
    })

    // Update user profile with new organization
    // TODO: refresh profile

    showCreateOrgDialog.value = false
    orgForm.value = {
      name: '',
      slug: ''
    }
  } catch (error) {
    console.error('Error creating organization:', error)
  } finally {
    isCreatingOrg.value = false
  }
}
</script>