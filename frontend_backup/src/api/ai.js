import apiClient from './client'

export const aiAPI = {
  // Generate content for a section
  generateContent(sectionId, context, prompt = null) {
    return apiClient.post(`/ai/generate/${sectionId}`, {
      section_name: '',
      context,
      prompt
    })
  },

  // Get field suggestions
  getSuggestions(fieldName, context) {
    return apiClient.post('/ai/suggestions', context, {
      params: { field_name: fieldName }
    })
  },

  // Auto-populate section from documents
  autoPopulate(sectionId, briefId) {
    return apiClient.post(`/ai/auto-populate/${sectionId}`, null, {
      params: { brief_id: briefId }
    })
  }
}
