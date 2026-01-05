import axios from 'axios'

// Force HTTPS for production
const getBackendURL = () => {
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname
    
    // Always use HTTPS for emergentagent.com domains
    if (hostname.includes('emergentagent.com')) {
      return `https://${hostname}`
    }
    
    // For localhost development
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return `http://${hostname}:8001`
    }
  }
  
  // Fallback - always HTTPS
  return 'https://basic-spec-builder.preview.emergentagent.com'
}

const BACKEND_URL = getBackendURL()

console.log('Backend URL configured as:', BACKEND_URL)

// Ensure baseURL always starts with https:// for production
const baseURL = BACKEND_URL.startsWith('http://') && BACKEND_URL.includes('emergentagent.com')
  ? BACKEND_URL.replace('http://', 'https://')
  : `${BACKEND_URL}/api`

console.log('API Base URL:', baseURL)

const apiClient = axios.create({
  baseURL: baseURL,
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
