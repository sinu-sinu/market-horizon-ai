import axios from 'axios'
import type { AxiosInstance, AxiosError } from 'axios'
import type { ApiError } from '@/types'

// Create axios instance with defaults
const api: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 120000, // 2 minute timeout for long-running analysis
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    // Handle common errors
    if (error.response) {
      const status = error.response.status
      const detail = error.response.data?.detail || 'An error occurred'

      switch (status) {
        case 400:
          console.error('Bad Request:', detail)
          break
        case 401:
          console.error('Unauthorized:', detail)
          // Could redirect to login
          break
        case 404:
          console.error('Not Found:', detail)
          break
        case 500:
          console.error('Server Error:', detail)
          break
        default:
          console.error('API Error:', detail)
      }
    } else if (error.request) {
      console.error('Network Error: No response received')
    } else {
      console.error('Request Error:', error.message)
    }

    return Promise.reject(error)
  }
)

export default api
