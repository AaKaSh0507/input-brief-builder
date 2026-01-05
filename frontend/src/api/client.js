import axios from 'axios'

// Get backend URL - prioritize VITE_ prefix for Vite, fallback to hardcoded production URL
const getBackendURL = () => {
  // Check if we're in the browser
  if (typeof window !== 'undefined') {
    // In production, use the preview URL
    if (window.location.hostname.includes('emergentagent.com')) {
      return window.location.origin
    }
  }
  
  // For development
  return import.meta.env.VITE_BACKEND_URL || 
         process.env.REACT_APP_BACKEND_URL || 
         'https://basic-spec-builder.preview.emergentagent.com'
}

const BACKEND_URL = getBackendURL()

console.log('Backend URL configured as:', BACKEND_URL)

const apiClient = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  headers: {
    'Content-Type': 'application/json'
  }
})

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
