import apiClient from './client'

export const sectionsAPI = {
  // Get sections for a brief
  getByBrief(briefId) {
    return apiClient.get(`/sections/brief/${briefId}`)
  },

  // Get single section
  getOne(id) {
    return apiClient.get(`/sections/${id}`)
  },

  // Create section
  create(briefId, data) {
    return apiClient.post(`/sections/`, data, {
      params: { brief_id: briefId }
    })
  },

  // Update section
  update(id, data) {
    return apiClient.put(`/sections/${id}`, data)
  },

  // Delete section
  delete(id) {
    return apiClient.delete(`/sections/${id}`)
  }
}
