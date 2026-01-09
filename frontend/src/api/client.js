import axios from 'axios'

// Use Vite environment variable, fallback to local backend
const BACKEND_URL =
  import.meta.env.VITE_BACKEND_URL || 'http://localhost:8001'

console.log('Backend URL:', BACKEND_URL)

const apiClient = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  headers: {
    'Content-Type': 'application/json'
  }
})

console.log('API Client baseURL:', apiClient.defaults.baseURL)

// Request interceptor
apiClient.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export default apiClient
