/**
 * Measurement types
 */

import type { SensorType, Metric, Unit } from './structure'

/**
 * Raw sensor data from API
 */
export interface RawSensorData {
  id: number
  name: string
  type_id: number
  [key: `metric_${number}`]: number | null
}

/**
 * Metric measurement with full metadata
 */
export interface MetricValue {
  value: number
  metric: Metric
  unit: Unit
}

/**
 * Transformed Sensor with mapped relationships
 */
export interface Sensor {
  id: number
  name: string
  type: SensorType | null
  [key: `metric_${number}`]: MetricValue | undefined
}

export interface MeasurementsResponse {
  data: RawSensorData[]
}

export interface MeasurementFilters {
  sensor_id?: string
  type_id?: string
  start_date?: string
  end_date?: string
  [key: string]: string | undefined
}
