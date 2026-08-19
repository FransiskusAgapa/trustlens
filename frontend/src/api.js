import axios from 'axios'

// VITE_API_URL is set in Render's build environment for production
// Falls back to localhost for local development
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
    timeout: 10000 // 10 second timeout on every request
})

export default api