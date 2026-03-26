/**
 * Sensors data composable — fetches sensor rows and exposes DataProvider + table template.
 */

import { ref, readonly, type DeepReadonly, type Ref } from 'vue'
import { apiClient } from '@/services/api'
import type { Sensor } from '@/types/sensor'
import type { DataProvider } from '@/types/provider'
import { mapRawSensorsToSensors } from '@/utils/sensorMapper'
import { SensorTableTemplate } from '@/templates/SensorTableTemplate'

export function useSensors(): DataProvider<Sensor> {
  const data = ref<Sensor[]>([])
  const isLoading = ref(false)
  const error = ref<Error | null>(null)

  /**
   * Fetch sensor rows from the API (replaces existing data).
   */
  const fetch = async (): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await apiClient.getSensors()
      data.value = mapRawSensorsToSensors(response.data)
    } catch (e) {
      error.value = e instanceof Error ? e : new Error('Failed to load sensors')
      console.error('Failed to load sensors:', e)
      data.value = []
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Re-fetch sensor rows
   */
  const refresh = async (): Promise<void> => {
    await fetch()
  }

  /**
   * Clear all data
   */
  const clear = (): void => {
    data.value = []
    error.value = null
  }

  return {
    data: readonly(data) as DeepReadonly<Ref<Sensor[]>>,
    isLoading: readonly(isLoading) as DeepReadonly<Ref<boolean>>,
    error: readonly(error) as DeepReadonly<Ref<Error | null>>,
    fetch,
    refresh,
    clear,
    tableTemplate: SensorTableTemplate,
  }
}
