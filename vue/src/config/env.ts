/**
 * Environment configuration
 * Centralized access to environment variables
 */

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const env = {
  apiUrl: apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl,
} as const

/**
 * Validate required environment variables
 */
export function validateEnv(): void {
  if (!env.apiUrl) {
    throw new Error('VITE_API_URL is required but not defined')
  }
}

// Validate on module load in development
if (import.meta.env.DEV) {
  validateEnv()
}
