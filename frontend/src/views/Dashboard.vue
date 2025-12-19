<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-900" data-testid="dashboard-title">GPJ Input Brief Assistant</h1>
          <button
            @click="createNewBrief"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            data-testid="create-brief-button"
          >
            + New Brief
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200" data-testid="stats-total">
          <p class="text-sm text-gray-600">Total Briefs</p>
          <p class="text-3xl font-bold text-gray-900 mt-2">{{ briefs.length }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200" data-testid="stats-draft">
          <p class="text-sm text-gray-600">Draft</p>
          <p class="text-3xl font-bold text-yellow-600 mt-2">{{ draftBriefs.length }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200" data-testid="stats-active">
          <p class="text-sm text-gray-600">In Progress</p>
          <p class="text-3xl font-bold text-blue-600 mt-2">{{ activeBriefs.length }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200" data-testid="stats-completed">
          <p class="text-sm text-gray-600">Completed</p>
          <p class="text-3xl font-bold text-green-600 mt-2">{{ completedBriefs.length }}</p>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="mb-6">
        <div class="flex space-x-4 border-b border-gray-200">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            @click="selectedTab = tab.value"
            :class="[
              'px-4 py-2 font-medium transition-colors',
              selectedTab === tab.value
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            ]"
            :data-testid="`filter-tab-${tab.value}`"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <!-- Briefs List -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div v-if="loading" class="p-8 text-center text-gray-500">
          Loading briefs...
        </div>

        <div v-else-if="filteredBriefs.length === 0" class="p-8 text-center text-gray-500">
          No briefs found. Create your first brief to get started!
        </div>

        <div v-else class="divide-y divide-gray-200">
          <div
            v-for="brief in filteredBriefs"
            :key="brief.id"
            class="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
            @click="openBrief(brief.id)"
            :data-testid="`brief-item-${brief.id}`"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ brief.title }}</h3>
                <div class="flex items-center space-x-4 text-sm text-gray-600">
                  <span v-if="brief.event_type" class="flex items-center">
                    <span class="mr-1">📋</span> {{ brief.event_type }}
                  </span>
                  <span class="flex items-center">
                    <span class="mr-1">📅</span> {{ formatDate(brief.created_at) }}
                  </span>
                  <span class="flex items-center">
                    <span class="mr-1">🔄</span> v{{ brief.version }}
                  </span>
                </div>
              </div>
              <div class="flex items-center space-x-3">
                <span
                  :class="[
                    'px-3 py-1 rounded-full text-xs font-medium',
                    getStatusClass(brief.status)
                  ]"
                  :data-testid="`brief-status-${brief.id}`"
                >
                  {{ brief.status.replace('_', ' ').toUpperCase() }}
                </span>
                <button
                  @click.stop="deleteBriefConfirm(brief.id)"
                  class="text-red-600 hover:text-red-800"
                  :data-testid="`delete-brief-${brief.id}`"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBriefStore } from '../stores/briefStore'
import { storeToRefs } from 'pinia'

const router = useRouter()
const briefStore = useBriefStore()
const { briefs, loading, activeBriefs, completedBriefs, draftBriefs } = storeToRefs(briefStore)

const selectedTab = ref('all')

const tabs = [
  { label: 'All Briefs', value: 'all' },
  { label: 'Draft', value: 'draft' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' }
]

const filteredBriefs = computed(() => {
  if (selectedTab.value === 'all') return briefs.value
  return briefs.value.filter(b => b.status === selectedTab.value)
})

const createNewBrief = () => {
  router.push('/brief/new')
}

const openBrief = (id) => {
  router.push(`/brief/${id}`)
}

const deleteBriefConfirm = async (id) => {
  if (confirm('Are you sure you want to delete this brief?')) {
    try {
      await briefStore.deleteBrief(id)
    } catch (error) {
      alert('Failed to delete brief')
    }
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getStatusClass = (status) => {
  const classes = {
    draft: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    archived: 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

onMounted(() => {
  briefStore.fetchBriefs()
})
</script>
