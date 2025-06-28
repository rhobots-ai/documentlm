<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">

    <!-- Sidebar -->
    <LayoutSidebar
        ref="sideBarRef"
        :is-sidebar-open="isSidebarOpen"
        :is-dark="isDark"
        :organization="whiteLabeledOrganization"
        :is-white-labeled="isWhiteLabeled"
        @update:is-dark="isDark = $event"
        @update:is-sidebar-open="isSidebarOpen = $event"
    />

    <!-- Main Content -->
    <main class="pt-12 md:pl-12" :class="{ 'lg:pl-64': isSidebarOpen }">
      <div v-if="isSidebarOpen && isMobile" class="fixed z-10 inset-0 bg-black/25"></div>
      <!-- App Bar -->
      <div
          class="fixed top-0 right-0 z-10 transition-[width] duration-500 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b border-gray-200/60 dark:border-gray-700/60"
          :class="{
          'w-[calc(100vw-16rem)]': isSidebarOpen,
          'w-full': !isSidebarOpen
        }">
        <div class="flex items-center justify-between h-12 px-4">
          <div class="flex items-center gap-3">
            <button
                v-show="!isSidebarOpen"
                class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                @click="isSidebarOpen = !isSidebarOpen"
            >
              <PanelLeft class="h-5 w-5 text-gray-600 dark:text-gray-400"/>
            </button>
            <NuxtLink to="/" class="flex items-center">
              <img
                  :src="isWhiteLabeled && whiteLabeledOrganization?.metadata
                      ? (isDark ? whiteLabeledOrganization.metadata.logo_dark : whiteLabeledOrganization.metadata.logo_light)
                      : (isDark ? '/images/logo-text-dark.svg' : '/images/logo-text-light.svg')"
                  alt="Logo"
                  :class="{
                        'h-8': isWhiteLabeled,
                        'h-6': !isWhiteLabeled
                    }"
              />
            </NuxtLink>
          </div>
          <NuxtLink
              v-show="!isSidebarOpen"
              to="/"
              class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
              :class="$route.path === '/' ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
          >
            <SquarePen class="h-5 w-5"/>
          </NuxtLink>
        </div>
      </div>
      <div class="relative">
        <slot/>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import {PanelLeft, SquarePen} from 'lucide-vue-next'
import {onClickOutside, useWindowSize} from "@vueuse/core";
import {useOrganizationStore} from '~/stores/organizations'
import {storeToRefs} from 'pinia'

const {width} = useWindowSize()
const organizationStore = useOrganizationStore()
const {whiteLabeledOrganization, isWhiteLabeled} = storeToRefs(organizationStore)

const isMobile = computed(() => width.value < 1024)

// const isSidebarOpen = ref(!isMobile.value && !isStudioPage.value)
const isSidebarOpen = ref(!isMobile.value)
const isDark = ref(false)
const sideBarRef = ref<HTMLElement | null>(null)

onMounted(() => {
  // Check for saved theme preference or system preference
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  isDark.value = savedTheme === 'dark' || (!savedTheme && prefersDark)
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  }
})

// Watch for screen size changes
watch(isMobile, (newValue) => {
  // isSidebarOpen.value = !newValue && !isStudioPage.value;
  isSidebarOpen.value = !newValue;
})

onClickOutside(sideBarRef, () => {
  if (isSidebarOpen.value && isMobile.value) {
    isSidebarOpen.value = false;
  }
})
</script>