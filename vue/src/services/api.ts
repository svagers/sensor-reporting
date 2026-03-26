/**
 * API Client Service
 * Centralized HTTP client for all API calls
 */

import { env } from '@/config/env'
import type { StructureData } from '@/types/structure'
import type { MeasurementsResponse, MeasurementFilters } from '@/types/measurement'

class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: unknown
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new ApiError(
          `API request failed: ${response.statusText}`,
          response.status,
          errorData
        )
      }

      return await response.json()
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }
      throw new ApiError(
        error instanceof Error ? error.message : 'Unknown error occurred'
      )
    }
  }

  async getStructure(): Promise<StructureData> {
    return this.request<StructureData>('/structure')
  }

  async getMeasurements(filters?: MeasurementFilters): Promise<MeasurementsResponse> {
    return this.request<MeasurementsResponse>('/measurements', {
      method: 'POST',
      body: JSON.stringify(filters || {}),
    })
  }
}

export const apiClient = new ApiClient(env.apiUrl)
export { ApiError }
