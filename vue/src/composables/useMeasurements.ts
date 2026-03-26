/**
 * Measurements Composable
 * Handles fetching and filtering measurement data
 * Implements DataProvider interface for use with generic components
 */

import { ref, readonly, type DeepReadonly, type Ref } from 'vue'
import { apiClient } from '@/services/api'
import type { Sensor, MeasurementFilters } from '@/types/measurement'
import type { DataProvider } from '@/types/provider'
import type { Column } from '@/types/column'
import { mapRawSensorsToSensors } from '@/utils/sensorMapper'
import PlainHeaderCell from '@/components/ui/cells/PlainHeaderCell.vue'
import MetricHeaderCell from '@/components/app/cells/MetricHeaderCell.vue'
import MetricCell from '@/components/app/cells/MetricCell.vue'
import SensorCell from '@/components/app/cells/SensorCell.vue'
import { structure } from '@/stores/structure'

export function useMeasurements(): DataProvider<Sensor, MeasurementFilters> {
  const data = ref<Sensor[]>([])
  const isLoading = ref(false)
  const error = ref<Error | null>(null)
  const currentFilters = ref<MeasurementFilters>({})

  /**
   * Fetch measurements with optional filters
   * Replaces existing data with new results
   */
  const fetch = async (filters?: MeasurementFilters): Promise<void> => {
    isLoading.value = true
    error.value = null
    currentFilters.value = filters || {}

    try {
      const response = await apiClient.getMeasurements(filters)
      data.value = mapRawSensorsToSensors(response.data)
    } catch (e) {
      error.value = e instanceof Error ? e : new Error('Failed to load measurements')
      console.error('Failed to load measurements:', e)
      data.value = []
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Refresh with current filters
   */
  const refresh = async (): Promise<void> => {
    await fetch(currentFilters.value)
  }

  /**
   * Clear all data and filters
   */
  const clear = (): void => {
    data.value = []
    currentFilters.value = {}
    error.value = null
  }

  /**
   * Get column definitions based on loaded data
   */
  const getColumns = (): Column[] => {
    const columns: Column[] = []

    columns.push({
      columnKey: 'name',
      sortKey: (row) => row.name,
      headerComponent: PlainHeaderCell,
      headerProps: {
        label: 'Sensor',
        columnKey: 'name',
      },
      cellComponent: SensorCell,
    })

    // Add columns for all metrics from structure
    if (structure.value?.metrics) {
      structure.value.metrics.forEach(metric => {
        columns.push({
          columnKey: `metric_${metric.id}`,
          sortKey: (row) => row[`metric_${metric.id}`]?.value ?? null,
          headerComponent: MetricHeaderCell,
          headerProps: {
            metric,
          },
          cellComponent: MetricCell,
          cellProps: {
            metricKey: `metric_${metric.id}`,
          },
        })
      })
    }

    return columns
  }

  return {
    data: readonly(data) as DeepReadonly<Ref<Sensor[]>>,
    isLoading: readonly(isLoading) as DeepReadonly<Ref<boolean>>,
    error: readonly(error) as DeepReadonly<Ref<Error | null>>,
    currentFilters: readonly(currentFilters) as DeepReadonly<Ref<MeasurementFilters>>,
    fetch,
    refresh,
    clear,
    getColumns,
  }
}
