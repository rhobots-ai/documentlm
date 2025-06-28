<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
      <!-- Hero Section -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-6xl font-bold bg-gradient-to-r from-primary-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
          Talk to Your Data. All of It.
        </h1>
        <p class="mt-6 text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-4">
          From scattered PDFs to hours of videos, DeepCite transforms chaos into clarity.
        </p>
        <p class="text-lg text-gray-500 dark:text-gray-400">
          Meet our team, see a live demo of DeepCite Enterprise, and get your questions answered.
        </p>
      </div>

      <div class="max-w-4xl mx-auto">
        <!-- Topics Section -->
        <div class="space-y-12">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100 text-center">Some Topics We'll Cover on Our Call</h2>

          <!-- Platform Overview -->
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-2xl opacity-10"></div>
            <div class="relative p-6 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
              <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
                <Server class="h-5 w-5 text-blue-500" />
                Overview of DeepCite Enterprise Platform
              </h3>
              <ul class="space-y-2 text-gray-600 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Architecture overview and deployment options (cloud, private cloud, on-premise)
                </li>
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Supported data types: text, PDFs, docs, images, audio, video, spreadsheets, and more
                </li>
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Custom agent workflows and integration pipelines
                </li>
              </ul>
            </div>
          </div>

          <!-- Security -->
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl opacity-10"></div>
            <div class="relative p-6 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
              <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
                <Shield class="h-5 w-5 text-purple-500" />
                Security, Privacy, and Compliance
              </h3>
              <ul class="space-y-2 text-gray-600 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Our enterprise-grade security protocols and access control models
                </li>
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Data residency, encryption standards, and compliance (SOC 2, HIPAA, etc.)
                </li>
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  How DeepCite ensures zero data leakage and end-to-end privacy
                </li>
              </ul>
            </div>
          </div>

          <!-- Use Cases -->
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl opacity-10"></div>
            <div class="relative p-6 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
              <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
                <Lightbulb class="h-5 w-5 text-emerald-500" />
                Explore Popular Enterprise Use Cases
              </h3>
              <ul class="space-y-2 text-gray-600 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Legal & Compliance: Summarize long legal documents and extract obligations
                </li>
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Media & Broadcasting: Search across transcripts, audio files, and video archives
                </li>
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Finance & Operations: Analyze Excel reports, PDFs, and meeting recordings
                </li>
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  R&D & Innovation Teams: Centralize unstructured research for faster insights
                </li>
                <li class="flex items-start gap-2">
                  <CheckCircle2 class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                  Internal Knowledge Management: Build a private ChatGPT over your internal data
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="mt-16 relative">
          <div class="absolute inset-0 bg-gradient-to-r from-primary-500 to-purple-500 rounded-2xl opacity-10"></div>
          <div class="relative p-8 rounded-2xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
            <form @submit.prevent="handleSubmit" class="space-y-6">
              <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-6">Contact Enterprise Team</h2>

              <!-- Name Fields -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">First Name *</label>
                  <input
                      v-model="form.firstName"
                      type="text"
                      required
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Last Name *</label>
                  <input
                      v-model="form.lastName"
                      type="text"
                      required
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>
              </div>

              <!-- Phone & Email -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone Number *</label>
                  <div class="flex relative">
                    <input
                        v-model="form.countryCode"
                        type="text"
                        placeholder="ISD Code"
                        class="w-24 rounded-l-lg border border-r-0 border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                    />
                    <input
                        v-model="form.phone"
                        type="tel"
                        required
                        class="w-full rounded-none rounded-r-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                        placeholder="Phone number"
                    />
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Work Email *</label>
                  <input
                      v-model="form.email"
                      type="email"
                      required
                      class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>
              </div>

              <!-- Use Cases -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">What are you interested in using DeepCite for? *</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  <button
                      v-for="useCase in useCases"
                      :key="useCase.id"
                      type="button"
                      class="relative p-4 rounded-lg border-2 transition-all text-left"
                      :class="[
                      selectedUseCases.includes(useCase.id)
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/50 dark:border-primary-400'
                        : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                    ]"
                      @click="toggleUseCase(useCase.id)"
                  >
                    <div class="flex items-start gap-3">
                      <component :is="useCase.icon" class="h-8 w-8 mt-0.5" :class="[
                        selectedUseCases.includes(useCase.id)
                          ? 'text-primary-600 dark:text-primary-400'
                          : 'text-gray-600 dark:text-gray-700'
                      ]" />
                      <div>
                        <div class="font-medium text-gray-900 dark:text-gray-100">{{ useCase.title }}</div>
                        <div class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ useCase.description }}</div>
                      </div>
                    </div>
                    <div
                        v-show="selectedUseCases.includes(useCase.id)"
                        class="absolute top-2 right-2 h-5 w-5 text-primary-600 dark:text-primary-400"
                    >
                      <CheckCircle2 class="h-5 w-5" />
                    </div>
                  </button>
                </div>
                <p v-if="useCaseError" class="mt-1 text-sm text-red-600 dark:text-red-400">
                  Please select at least one use case
                </p>
              </div>

              <!-- Source -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">How did you hear about us?</label>
                <input
                    v-model="form.source"
                    type="text"
                    placeholder="Friend, conference, current user, etc?"
                    class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500"
                />
              </div>

              <!-- Submit Button -->
              <button
                  type="submit"
                  class="w-full px-6 py-3 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
                  :disabled="isSubmitting"
              >
                <Loader2 v-if="isSubmitting" class="h-4 w-4 animate-spin" />
                {{ isSubmitting ? 'Sending...' : 'Contact Enterprise Team' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Server, Shield, Lightbulb, CheckCircle2, Loader2, Search, FileText, Brain, MessageSquare, Database, Code, Lock } from 'lucide-vue-next'

definePageMeta({
  layout: 'header'
})

const isSubmitting = ref(false)
const useCaseError = ref(false)
const selectedUseCases = ref<string[]>([])

const useCases = [
  {
    id: 'document-understanding',
    icon: Search,
    title: 'Document Understanding & Research',
    description: 'Summarizing documents, extracting key information, semantic search'
  },
  {
    id: 'media-analysis',
    icon: FileText,
    title: 'Media & Audio Analysis',
    description: 'Transcribing and analyzing video/audio content, searching spoken content'
  },
  {
    id: 'data-extraction',
    icon: Database,
    title: 'Unstructured Data Extraction',
    description: 'Parsing PDFs, extracting tables and forms, processing handwritten documents'
  },
  {
    id: 'ai-assistant',
    icon: Brain,
    title: 'AI Knowledge Assistant',
    description: 'Internal ChatGPT, knowledge assistant for support, legal, HR'
  },
  {
    id: 'enterprise-intelligence',
    icon: MessageSquare,
    title: 'Enterprise Intelligence',
    description: 'Integration with enterprise systems, real-time querying, insights'
  },
  {
    id: 'developer-integration',
    icon: Code,
    title: 'Developer / API Integration',
    description: 'Embedding in internal tools, custom workflows, API integration'
  },
  {
    id: 'security-compliance',
    icon: Lock,
    title: 'Security & Compliance',
    description: 'On-premise deployment, role-based access, compliance (SOC 2, HIPAA)'
  }
]

const toggleUseCase = (id: string) => {
  const index = selectedUseCases.value.indexOf(id)
  if (index === -1) {
    selectedUseCases.value.push(id)
  } else {
    selectedUseCases.value.splice(index, 1)
  }
  useCaseError.value = false
}

const form = ref({
  firstName: '',
  lastName: '',
  countryCode: '',
  phone: '',
  email: '',
  source: ''
})


const handleSubmit = async () => {
  if (selectedUseCases.value.length === 0) {
    useCaseError.value = true
    return
  }

  isSubmitting.value = true

  try {
    // TODO: Implement form submission
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Reset form
    selectedUseCases.value = []
    form.value = {
      firstName: '',
      lastName: '',
      phone: '',
      email: '',
      source: ''
    }
  } catch (error) {
    console.error('Error submitting form:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>