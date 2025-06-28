import {defineStore} from 'pinia'
import {computed, ref} from 'vue'
import type {Organization} from "~/types/organization";
import {OrganizationsApi} from "~/api/organizations";
import {getSubdomain} from "~/utils/url";

export const useOrganizationStore = defineStore('organization', () => {
  const organization = ref<Organization | null>(null)
  const whiteLabeledOrganization = ref<Organization | null>(null)
  const whiteLabeledStatus = ref<'default' | 'not_enabled' | 'not_member' | 'enabled'>('default')
  const members = ref<any[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const api = new OrganizationsApi()

  // Getters
  const memberCount = computed(() => members.value.length)
  const pendingInvites = computed(() => members.value.filter(m => m.status === 'pending'))
  const isWhiteLabeled = computed(() => !!whiteLabeledOrganization.value?.metadata.is_white_labeled)

  // Actions
  async function fetchOrganization(id: string) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.getOrganization(id)
      if (apiError) {
        throw apiError
      }
      organization.value = data
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching organization:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchOrganizationBySlug(slug: string) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.getOrganizationBySlug(slug)
      if (apiError) {
        throw apiError
      }

      if (data['results']) {
        whiteLabeledOrganization.value = data['results'][0]
      }

      whiteLabeledStatus.value = !!whiteLabeledOrganization.value?.metadata.is_white_labeled ? 'enabled' : 'not_enabled'

      const userStore = useUserStore()
      const {profile} = storeToRefs(userStore)

      // check if it is org (subdomain) url and user is a member of the current org
      const subDomain = getSubdomain()
      if (false && whiteLabeledStatus.value == 'enabled' && profile.value && subDomain && subDomain !== 'deepcite') {
        const isCurrentUserOrganization = profile.value.organizations.filter(o => o.slug === subDomain).length > 0
        if (!isCurrentUserOrganization) {
          whiteLabeledStatus.value = 'not_member'
        }
      }

      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching organization by domain:', e)
      return null
    } finally {
      loading.value = false
    }
  }

  async function createOrganization(name: string, slug: string) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.createOrganization({
        name,
        slug
      })

      if (apiError) {
        throw apiError
      }

      organization.value = data
      return data
    } catch (e) {
      error.value = e as Error
      console.error('Error creating organization:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchMembers(id: string) {
    loading.value = true
    error.value = null

    try {
      const {data, error: apiError} = await api.getMembers(id)
      if (apiError) {
        throw apiError
      }
      members.value = data || []
    } catch (e) {
      error.value = e as Error
      console.error('Error fetching members:', e)
    } finally {
      loading.value = false
    }
  }

  async function inviteMember(id: string, email: string, role: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.inviteMember(id, email, role)
      if (apiError) {
        throw apiError
      }

      // Add pending member to list
      members.value.push({
        email,
        role,
        status: 'pending'
      })
    } catch (e) {
      error.value = e as Error
      console.error('Error inviting member:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function removeMember(id: string, userId: string) {
    loading.value = true
    error.value = null

    try {
      const {error: apiError} = await api.removeMember(id, userId)
      if (apiError) {
        throw apiError
      }

      // Remove member from list
      members.value = members.value.filter(m => m.id !== userId)
    } catch (e) {
      error.value = e as Error
      console.error('Error removing member:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    organization,
    whiteLabeledOrganization,
    whiteLabeledStatus,
    members,
    loading,
    error,

    // Getters
    memberCount,
    pendingInvites,
    isWhiteLabeled,

    // Actions
    fetchOrganization,
    fetchOrganizationBySlug,
    createOrganization,
    fetchMembers,
    inviteMember,
    removeMember
  }
})