import apiClient from './client'

export const documentsAPI = {
  // Get documents for a brief
  getByBrief(briefId) {
    return apiClient.get(`/documents/brief/${briefId}`)
  },

  // Get single document
  getOne(id) {
    return apiClient.get(`/documents/${id}`)
  },

  // Upload document
  upload(briefId, file) {
    const formData = new FormData()
    formData.append('file', file)
    
    return apiClient.post('/documents/upload', formData, {
      params: { brief_id: briefId },
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // Analyze document
  analyze(documentId, sectionName) {
    return apiClient.post(`/documents/${documentId}/analyze`, null, {
      params: { section_name: sectionName }
    })
  },

  // Delete document
  delete(id) {
    return apiClient.delete(`/documents/${id}`)
  }
}
