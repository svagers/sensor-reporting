/**
 * Environment configuration
 * Centralized access to environment variables
 */

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const normalizedApiUrl = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl

/** Origin of the API server (e.g. http://localhost:8000) for links outside `/api`. */
const apiOrigin = new URL(normalizedApiUrl).origin

/** Swagger UI (OpenAPI) — same as Django root `/` and `/api/docs/`. */
const apiDocsUrl = `${apiOrigin}/api/docs/`

export const env = {
  apiUrl: normalizedApiUrl,
  apiOrigin,
  apiDocsUrl,
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
