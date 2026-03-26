/**
 * API Client Service
 * Centralized HTTP client for all API calls.
 */

import { env } from '@/config/env'
import { markApiReachable, markApiUnreachable } from '@/stores/connection'
import { showErrorToast } from '@/stores/toast'
import type { SensorType, Metric } from '@/types/structure'
import type { RawSensorData } from '@/types/sensor'

/** GET /structure response body */
export interface StructureData {
  sensor_types: SensorType[]
  metrics: Metric[]
}

/** GET /measurements response body */
export interface SensorsResponse {
  data: RawSensorData[]
}

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

function isNetworkFailure(error: unknown): boolean {
  if (error instanceof ApiError) return false
  if (error instanceof DOMException && error.name === 'AbortError') return false
  const msg = error instanceof Error ? error.message : String(error)
  if (/failed to fetch|networkerror|load failed|connection refused|net::err/i.test(msg)) {
    return true
  }
  if (error instanceof TypeError) return true
  return false
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

      markApiReachable()

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        showErrorToast(
          'Request failed',
          `The server returned ${response.status} ${response.statusText}.`
        )
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
      if (isNetworkFailure(error)) {
        markApiUnreachable()
      } else {
        showErrorToast(
          'Request failed',
          error instanceof Error ? error.message : 'Unknown error occurred'
        )
      }
      throw new ApiError(
        error instanceof Error ? error.message : 'Unknown error occurred'
      )
    }
  }

  async getStructure(): Promise<StructureData> {
    return this.request<StructureData>('/structure')
  }

  async getSensors(): Promise<SensorsResponse> {
    return this.request<SensorsResponse>('/measurements')
  }
}

export const apiClient = new ApiClient(env.apiUrl)
export { ApiError }
