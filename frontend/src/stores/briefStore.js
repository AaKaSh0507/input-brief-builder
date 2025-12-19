import { defineStore } from 'pinia'
import { briefsAPI } from '../api/briefs'
import { sectionsAPI } from '../api/sections'
import { documentsAPI } from '../api/documents'

export const useBriefStore = defineStore('brief', {
  state: () => ({
    briefs: [],
    currentBrief: null,
    currentSections: [],
    currentDocuments: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchBriefs(status = null) {
      this.loading = true
      this.error = null
      try {
        const response = await briefsAPI.getAll(status)
        this.briefs = response.data
      } catch (error) {
        this.error = error.message
        console.error('Error fetching briefs:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchBrief(id) {
      this.loading = true
      this.error = null
      try {
        const response = await briefsAPI.getOne(id)
        this.currentBrief = response.data
        
        // Also fetch sections and documents
        await this.fetchSections(id)
        await this.fetchDocuments(id)
      } catch (error) {
        this.error = error.message
        console.error('Error fetching brief:', error)
      } finally {
        this.loading = false
      }
    },

    async createBrief(data) {
      this.loading = true
      this.error = null
      try {
        const response = await briefsAPI.create(data)
        this.currentBrief = response.data
        await this.fetchSections(response.data.id)
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('Error creating brief:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateBrief(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await briefsAPI.update(id, data)
        this.currentBrief = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('Error updating brief:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteBrief(id) {
      this.loading = true
      this.error = null
      try {
        await briefsAPI.delete(id)
        this.briefs = this.briefs.filter(b => b.id !== id)
      } catch (error) {
        this.error = error.message
        console.error('Error deleting brief:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchSections(briefId) {
      try {
        const response = await sectionsAPI.getByBrief(briefId)
        this.currentSections = response.data
      } catch (error) {
        console.error('Error fetching sections:', error)
      }
    },

    async updateSection(sectionId, data) {
      try {
        const response = await sectionsAPI.update(sectionId, data)
        const index = this.currentSections.findIndex(s => s.id === sectionId)
        if (index !== -1) {
          this.currentSections[index] = response.data
        }
        return response.data
      } catch (error) {
        console.error('Error updating section:', error)
        throw error
      }
    },

    async fetchDocuments(briefId) {
      try {
        const response = await documentsAPI.getByBrief(briefId)
        this.currentDocuments = response.data
      } catch (error) {
        console.error('Error fetching documents:', error)
      }
    },

    async uploadDocument(briefId, file) {
      try {
        const response = await documentsAPI.upload(briefId, file)
        this.currentDocuments.push(response.data)
        return response.data
      } catch (error) {
        console.error('Error uploading document:', error)
        throw error
      }
    },

    async exportBrief(id, format = 'pdf') {
      try {
        const response = await briefsAPI.exportBrief(id, format)
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `brief_${id}.${format}`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (error) {
        console.error('Error exporting brief:', error)
        throw error
      }
    }
  },

  getters: {
    activeBriefs: (state) => state.briefs.filter(b => b.status === 'in_progress'),
    completedBriefs: (state) => state.briefs.filter(b => b.status === 'completed'),
    draftBriefs: (state) => state.briefs.filter(b => b.status === 'draft')
  }
})
