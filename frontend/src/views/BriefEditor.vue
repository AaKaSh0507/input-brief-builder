<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <div>
            <button
              @click="goBack"
              class="text-blue-600 hover:text-blue-800 mb-2 flex items-center"
              data-testid="back-button"
            >
              ← Back to Dashboard
            </button>
            <h1 class="text-2xl font-bold text-gray-900" data-testid="brief-title">
              {{ isNewBrief ? 'New Brief' : currentBrief?.title || 'Loading...' }}
            </h1>
          </div>
          <div class="flex space-x-3">
            <button
              v-if="!isNewBrief"
              @click="exportBrief('pdf')"
              class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
              data-testid="export-pdf-button"
            >
              Export PDF
            </button>
            <button
              v-if="!isNewBrief"
              @click="exportBrief('word')"
              class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
              data-testid="export-word-button"
            >
              Export Word
            </button>
            <button
              @click="saveBrief"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              :disabled="saving"
              data-testid="save-brief-button"
            >
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <p class="text-gray-500">Loading...</p>
    </div>

    <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Sidebar - Section Navigation -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 sticky top-24">
            <h2 class="font-semibold text-gray-900 mb-4">Sections</h2>
            <nav class="space-y-1">
              <button
                v-for="section in currentSections"
                :key="section.id"
                @click="currentSectionIndex = section.section_number - 1"
                :class="[
                  'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors',
                  currentSectionIndex === section.section_number - 1
                    ? 'bg-blue-100 text-blue-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-100'
                ]"
                :data-testid="`section-nav-${section.section_number}`"
              >
                {{ section.section_number }}. {{ section.section_name }}
              </button>
            </nav>
          </div>
        </div>

        <!-- Main Content - Current Section -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <div v-if="currentSection">
              <div class="flex justify-between items-start mb-6">
                <div>
                  <h2 class="text-xl font-bold text-gray-900" data-testid="section-title">
                    {{ currentSection.section_number }}. {{ currentSection.section_name }}
                  </h2>
                  <p class="text-sm text-gray-600 mt-1">
                    Fill in the information below or use AI assistance
                  </p>
                </div>
                <div class="flex space-x-2">
                  <button
                    v-if="!isNewBrief && currentDocuments.length > 0"
                    @click="autoPopulateSection"
                    class="px-3 py-1 bg-purple-600 text-white text-sm rounded hover:bg-purple-700"
                    :disabled="aiLoading"
                    data-testid="auto-populate-button"
                  >
                    {{ aiLoading ? 'Processing...' : '✨ Auto-populate from docs' }}
                  </button>
                  <button
                    @click="generateAIContent"
                    class="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                    :disabled="aiLoading"
                    data-testid="generate-ai-button"
                  >
                    {{ aiLoading ? 'Generating...' : '🤖 Generate AI' }}
                  </button>
                </div>
              </div>

              <!-- Section Content Editor -->
              <div class="space-y-4">
                <div v-for="(value, field) in sectionContent" :key="field" class="border-b border-gray-200 pb-4">
                  <label :for="field" class="block text-sm font-medium text-gray-700 mb-2">
                    {{ formatFieldName(field) }}
                  </label>
                  <textarea
                    :id="field"
                    v-model="sectionContent[field]"
                    rows="3"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    :placeholder="`Enter ${formatFieldName(field).toLowerCase()}`"
                    :data-testid="`field-${field}`"
                  ></textarea>
                </div>

                <!-- Add Field Button -->
                <button
                  @click="addCustomField"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  data-testid="add-field-button"
                >
                  + Add Custom Field
                </button>
              </div>

              <!-- AI Generated Suggestions -->
              <div v-if="Object.keys(currentSection.ai_generated || {}).length > 0" class="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <h3 class="font-semibold text-blue-900 mb-2">💡 AI Suggestions</h3>
                <div class="text-sm text-blue-800 whitespace-pre-wrap">
                  {{ JSON.stringify(currentSection.ai_generated, null, 2) }}
                </div>
              </div>

              <!-- Navigation Buttons -->
              <div class="flex justify-between mt-8">
                <button
                  v-if="currentSectionIndex > 0"
                  @click="previousSection"
                  class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  data-testid="previous-section-button"
                >
                  ← Previous Section
                </button>
                <div v-else></div>
                <button
                  v-if="currentSectionIndex < currentSections.length - 1"
                  @click="nextSection"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  data-testid="next-section-button"
                >
                  Next Section →
                </button>
                <button
                  v-else
                  @click="completeBrief"
                  class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  data-testid="complete-brief-button"
                >
                  ✓ Complete Brief
                </button>
              </div>
            </div>
          </div>

          <!-- Document Upload Section -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="font-semibold text-gray-900 mb-4">📎 Uploaded Documents</h3>
            
            <div class="mb-4">
              <input
                type="file"
                @change="handleFileUpload"
                accept=".pdf,.doc,.docx,.xlsx,.xls,.csv,.ppt,.pptx,.png,.jpg,.jpeg"
                class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                :disabled="uploading || isNewBrief"
                data-testid="file-upload-input"
              />
              <p class="text-xs text-gray-500 mt-1">
                Supported: PDF, DOC, DOCX, EXCEL (.xlsx, .xls), CSV, PPT, PPTX, PNG, JPG
              </p>
              <p v-if="isNewBrief" class="text-xs text-orange-600 mt-1">
                ⚠️ Please save the brief first before uploading documents
              </p>
            </div>

            <div v-if="currentDocuments.length === 0" class="text-center text-gray-500 py-4">
              No documents uploaded yet
            </div>

            <div v-else class="space-y-2">
              <div
                v-for="doc in currentDocuments"
                :key="doc.id"
                class="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
                :data-testid="`document-${doc.id}`"
              >
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ doc.filename }}</p>
                  <p class="text-xs text-gray-500">{{ formatDate(doc.uploaded_at) }}</p>
                </div>
                <button
                  @click="deleteDocument(doc.id)"
                  class="text-red-600 hover:text-red-800 text-sm"
                  data-testid="`delete-document-${doc.id}`"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useBriefStore } from '../stores/briefStore'
import { storeToRefs } from 'pinia'
import { aiAPI } from '../api/ai'
import { documentsAPI } from '../api/documents'

const router = useRouter()
const route = useRoute()
const briefStore = useBriefStore()
const { currentBrief, currentSections, currentDocuments, loading } = storeToRefs(briefStore)

const isNewBrief = computed(() => route.params.id === 'new')
const currentSectionIndex = ref(0)
const sectionContent = ref({})
const saving = ref(false)
const uploading = ref(false)
const aiLoading = ref(false)

const currentSection = computed(() => {
  if (currentSections.value.length === 0) return null
  return currentSections.value[currentSectionIndex.value]
})

// Initialize section content when section changes
watch(currentSection, (newSection) => {
  if (newSection) {
    sectionContent.value = { ...newSection.content }
    if (Object.keys(sectionContent.value).length === 0) {
      // Initialize with default fields based on section
      sectionContent.value = getDefaultFields(newSection.section_name)
    }
  }
}, { immediate: true })

const getDefaultFields = (sectionName) => {
  // Return default fields based on section name
  return {
    description: '',
    notes: ''
  }
}

const formatFieldName = (field) => {
  return field.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const goBack = () => {
  router.push('/')
}

const saveBrief = async () => {
  saving.value = true
  try {
    // Save current section content
    if (currentSection.value) {
      await briefStore.updateSection(currentSection.value.id, {
        content: sectionContent.value
      })
    }
    alert('Brief saved successfully!')
  } catch (error) {
    alert('Failed to save brief')
  } finally {
    saving.value = false
  }
}

const previousSection = async () => {
  await saveCurrentSection()
  currentSectionIndex.value--
}

const nextSection = async () => {
  await saveCurrentSection()
  currentSectionIndex.value++
}

const saveCurrentSection = async () => {
  if (currentSection.value) {
    try {
      await briefStore.updateSection(currentSection.value.id, {
        content: sectionContent.value
      })
    } catch (error) {
      console.error('Error saving section:', error)
    }
  }
}

const completeBrief = async () => {
  await saveCurrentSection()
  await briefStore.updateBrief(currentBrief.value.id, {
    status: 'completed'
  })
  alert('Brief completed successfully!')
  router.push('/')
}

const generateAIContent = async () => {
  if (!currentSection.value) return
  
  aiLoading.value = true
  try {
    const response = await aiAPI.generateContent(currentSection.value.id, sectionContent.value)
    // Merge AI generated content with current content
    alert('AI content generated! Check the suggestions below.')
    await saveCurrentSection()
    await briefStore.fetchSections(currentBrief.value.id)
  } catch (error) {
    alert('Failed to generate AI content')
  } finally {
    aiLoading.value = false
  }
}

const autoPopulateSection = async () => {
  if (!currentSection.value || !currentBrief.value) return
  
  aiLoading.value = true
  try {
    const response = await aiAPI.autoPopulate(currentSection.value.id, currentBrief.value.id)
    alert('Section auto-populated from documents!')
    await briefStore.fetchSections(currentBrief.value.id)
  } catch (error) {
    alert('Failed to auto-populate section')
  } finally {
    aiLoading.value = false
  }
}

const addCustomField = () => {
  const fieldName = prompt('Enter field name:')
  if (fieldName) {
    const key = fieldName.toLowerCase().replace(/\s+/g, '_')
    sectionContent.value[key] = ''
  }
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  uploading.value = true
  try {
    await briefStore.uploadDocument(currentBrief.value.id, file)
    alert('Document uploaded successfully!')
  } catch (error) {
    alert('Failed to upload document')
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}

const deleteDocument = async (docId) => {
  if (confirm('Are you sure you want to delete this document?')) {
    try {
      await documentsAPI.delete(docId)
      await briefStore.fetchDocuments(currentBrief.value.id)
    } catch (error) {
      alert('Failed to delete document')
    }
  }
}

const exportBrief = async (format) => {
  try {
    await briefStore.exportBrief(currentBrief.value.id, format)
    alert(`Brief exported as ${format.toUpperCase()}!`)
  } catch (error) {
    alert('Failed to export brief')
  }
}

onMounted(async () => {
  // Check if we have a valid route parameter
  if (!route.params.id) {
    console.error('No brief ID in route')
    router.push('/')
    return
  }
  
  if (isNewBrief.value) {
    // Create new brief
    try {
      const title = prompt('Enter brief title:')
      if (!title) {
        router.push('/')
        return
      }
      const eventType = prompt('Enter event type (optional):')
      
      await briefStore.createBrief({
        title,
        event_type: eventType || null,
        brief_metadata: {}
      })
      
      // Update route to use the new brief ID
      if (briefStore.currentBrief && briefStore.currentBrief.id) {
        router.replace(`/brief/${briefStore.currentBrief.id}`)
      } else {
        throw new Error('Brief creation failed - no ID returned')
      }
    } catch (error) {
      console.error('Error creating brief:', error)
      alert('Failed to create brief')
      router.push('/')
    }
  } else {
    // Load existing brief
    try {
      await briefStore.fetchBrief(route.params.id)
    } catch (error) {
      console.error('Error loading brief:', error)
      alert('Brief not found')
      router.push('/')
    }
  }
})
</script>
