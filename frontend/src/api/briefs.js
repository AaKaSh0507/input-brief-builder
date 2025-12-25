import apiClient from './client'

export const briefsAPI = {
  // Get all briefs
  getAll(status = null, skip = 0, limit = 100) {
    const params = { skip, limit }
    if (status) params.status = status
    return apiClient.get('/briefs', { params })
  },

  // Get single brief
  getOne(id) {
    return apiClient.get(`/briefs/${id}`)
  },

  // Create brief
  create(data) {
    return apiClient.post('/briefs/', data)
  },

  // Update brief
  update(id, data) {
    return apiClient.put(`/briefs/${id}`, data)
  },

  // Delete brief
  delete(id) {
    return apiClient.delete(`/briefs/${id}`)
  },

  // Get versions
  getVersions(id) {
    return apiClient.get(`/briefs/${id}/versions`)
  },

  // Create version
  createVersion(id) {
    return apiClient.post(`/briefs/${id}/versions`)
  },

  // Export brief
  exportBrief(id, format = 'pdf') {
    return apiClient.get(`/briefs/${id}/export`, {
      params: { format },
      responseType: 'blob'
    })
  }
}
