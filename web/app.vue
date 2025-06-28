<template>
  <NuxtLoadingIndicator/>
  <NuxtLayout>
    <div v-if="isLoading" class="fixed inset-0 z-50 flex items-center justify-center bg-white dark:bg-gray-900">
      <!-- Your custom loader here -->
      <div role="status">
        <svg aria-hidden="true" class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-primary-500" viewBox="0 0 100 101" fill="none"
             xmlns="http://www.w3.org/2000/svg">
          <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="currentColor"/>
          <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentFill"/>
        </svg>
        <span class="sr-only">Loading...</span>
      </div>
    </div>
    <NuxtPage v-else/>
  </NuxtLayout>
</template>

<script setup lang="ts">
import {storeToRefs} from 'pinia'
import {useOrganizationStore} from '~/stores/organizations'
import {getSubdomain} from '~/utils/url'
import {useUserStore} from "~/stores/user";

const organizationStore = useOrganizationStore()
const {isWhiteLabeled, whiteLabeledOrganization, whiteLabeledStatus} = storeToRefs(organizationStore)
const isLoading = ref<boolean>(true)

const checkIfWhiteLabeled = async () => {
  try {
    const subDomain = getSubdomain()

    // Skip for localhost and common development domains
    if (!subDomain || subDomain === 'deepcite') {
      return
    }

    await organizationStore.fetchOrganizationBySlug(subDomain)
    if (whiteLabeledStatus.value === 'default') {
      return
    } else if (whiteLabeledStatus.value === 'not_enabled') {
      throw {status: 412, message: 'Not enabled'}
    } else if (whiteLabeledStatus.value === 'not_member') {
      throw {status: 403, message: 'You cannot access this page.'}
    } else {
      const {setColorPalette} = useTheme();
      setColorPalette(organizationStore.whiteLabeledOrganization?.metadata.theme || 'indigo')
    }
  } catch (error: any) {
    throw createError({
      fatal: true,
      statusCode: error.status,
      message: error.message
    });
  }
}

const forceLogOut = async (signOutFromAuth: boolean) => {
  if (signOutFromAuth) {
    const {signOut} = useAuthClient()
    await signOut()
  }

  const userStore = useUserStore()
  userStore.clearProfile()
}

const updateSession = async () => {
  try {
    const {getSession, setJwtToken, organization, useListOrganizations} = useAuthClient()

    await setJwtToken()

    let organizationsRef = useListOrganizations.get()
    while (organizationsRef.isPending) {
      await new Promise(resolve => setTimeout(resolve, 50));
      organizationsRef = useListOrganizations.get();
    }

    const organizations = organizationsRef.data || []

    // Set active organization if available
    if (organizations.length != 0) {
      await organization.setActive({
        organizationId: organizations[0].id
      })
    }

    // Get session data
    const session = await getSession({fetchOptions: {credentials: 'include'}})

    if (session.data) {
      const userStore = useUserStore()
      userStore.setProfile({
        ...session.data.user,
        organizations
      })
    }
  } catch (e: any) {
    await forceLogOut(e.status !== 401)
  }
}

onMounted(async () => {
  const script = document.createElement("script");
  script.src = "https://checkout.razorpay.com/v1/checkout.js";
  script.async = true;
  document.head.appendChild(script);

  await updateSession()
  await checkIfWhiteLabeled()
  isLoading.value = false
});

useHead({
  title: computed(() => isWhiteLabeled.value
      ? `${whiteLabeledOrganization.value?.name} – Talk to Your Data`
      : 'Talk to Your Data. Visualize Knowledge.'),
  meta: [
    {
      name: 'description',
      content: computed(() => isWhiteLabeled.value
          ? `${whiteLabeledOrganization.value?.name}, an AI-powered research assistant for document analysis.`
          : 'An AI-powered research assistant purpose-built for deep document analysis, citation accuracy, and real-time collaboration.')
    },
    {
      name: 'facebook-domain-verification',
      content: 'hb5mlnuhjn1wghk8lr2z7skfta7w38'
    }
  ]
})

useSeoMeta({
  title: computed(() => isWhiteLabeled.value
      ? `${whiteLabeledOrganization.value?.name} – Talk to Your Data`
      : 'Talk to Your Data. Visualize Knowledge.'),
  description: computed(() => isWhiteLabeled.value
      ? `${whiteLabeledOrganization.value?.name}, an AI-powered research assistant for document analysis.`
      : 'A purpose-built AI research assistant for dense documents, offering verified citations, fast answers, and secure collaboration.'),
  ogTitle: computed(() => isWhiteLabeled.value
      ? `${whiteLabeledOrganization.value?.name} – Talk to Your Data`
      : 'Talk to Your Data. Visualize Knowledge.'),
  ogDescription: computed(() => isWhiteLabeled.value
      ? `${whiteLabeledOrganization.value?.name}, an AI-powered research assistant for document analysis.`
      : 'Ask deep questions across data. Get citations. Collaborate securely. It is your AI assistant for serious research.'),
  ogImage: computed(() => isWhiteLabeled.value && whiteLabeledOrganization.value?.metadata
      ? whiteLabeledOrganization.value.metadata.logo_light
      : 'https://deepcite.rhobots.ai/images/og-image.png'),
  ogUrl: computed(() => isWhiteLabeled.value
      ? `https://${window.location.hostname}`
      : 'https://deepcite.rhobots.ai/'),
  ogType: 'website',
  twitterCard: 'summary_large_image',
  twitterTitle: computed(() => isWhiteLabeled.value
      ? `${whiteLabeledOrganization.value?.name} – AI-Powered Document Research Assistant`
      : 'AI-Powered Document Research Assistant'),
  twitterDescription: computed(() => isWhiteLabeled.value
      ? `Ask complex questions, get grounded answers, and cite confidently — all within ${whiteLabeledOrganization.value?.name}.`
      : 'Ask complex questions, get grounded answers, and cite confidently — all within your domain.'),
  twitterImage: computed(() => isWhiteLabeled.value && whiteLabeledOrganization.value?.metadata
      ? whiteLabeledOrganization.value.metadata.logo_light
      : 'https://deepcite.rhobots.ai/images/og-image.png'),
  robots: 'index, follow',
});
</script>