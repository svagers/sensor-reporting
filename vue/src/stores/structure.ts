/**
 * Structure Store
 * Simple reactive module for static global data
 * Loads once, accessible everywhere via direct import
 */

import { ref, readonly } from 'vue'
import { apiClient } from '@/services/api'
import type { StructureData, SensorType, Metric } from '@/types/structure'

const data = ref<StructureData | null>(null)
const isLoading = ref(false)
const error = ref<Error | null>(null)

let loadPromise: Promise<void> | null = null

/**
 * Load structure data (only once, even if called multiple times)
 */
export async function loadStructure(): Promise<void> {
  if (data.value || loadPromise) return loadPromise || Promise.resolve()

  isLoading.value = true
  error.value = null

  loadPromise = apiClient
    .getStructure()
    .then((response) => {
      data.value = response
    })
    .catch((e) => {
      error.value = e instanceof Error ? e : new Error('Failed to load structure data')
      console.error('Failed to load structure data:', e)
    })
    .finally(() => {
      isLoading.value = false
    })

  return loadPromise
}

/**
 * Get all sensor types
 */
export function getSensorTypes(): SensorType[] {
  return data.value?.sensor_types || []
}

/**
 * Get sensor type by ID
 */
export function getSensorTypeById(id: number): SensorType | undefined {
  return data.value?.sensor_types.find((st: SensorType) => st.id === id)
}

/**
 * Get metric by ID
 */
export function getMetricById(id: number): Metric | undefined {
  return data.value?.metrics.find((m: Metric) => m.id === id)
}

// Export readonly refs for reactive access
export const structure = readonly(data)
export const structureLoading = readonly(isLoading)
export const structureError = readonly(error)
