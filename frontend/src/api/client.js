import axios from 'axios'

// Hardcoded HTTPS URL for production - no dynamic detection
const BACKEND_URL = 'https://basic-spec-builder.preview.emergentagent.com'

console.log('Backend URL (hardcoded):', BACKEND_URL)

const apiClient = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  headers: {
    'Content-Type': 'application/json'
  }
})

console.log('API Client baseURL:', apiClient.defaults.baseURL)

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export default apiClient
