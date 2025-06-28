<template>
  <button
      class="w-full flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800"
      @click="toggleTheme"
  >
    <Sun v-if="isDark" class="h-4 w-4 text-gray-500 dark:text-gray-400"/>
    <Moon v-else class="h-4 w-4 text-gray-500 dark:text-gray-400"/>
    {{isDark ? 'Light' : 'Dark'}}
  </button>
</template>

<script setup lang="ts">
  import { Sun, Moon } from 'lucide-vue-next'

  const props = defineProps<{
    isDark: boolean
  }>()

  const emit = defineEmits<{
    (e: 'update:isDark', value: boolean): void
  }>()

  const toggleTheme = () => {
    const newValue = !props.isDark
    emit('update:isDark', newValue)
    document.documentElement.classList.toggle('dark')
    localStorage.setItem('theme', newValue ? 'dark' : 'light')
  }
</script>