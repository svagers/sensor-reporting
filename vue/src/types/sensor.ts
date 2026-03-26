/**
 * Sensor row types, API payloads, and metric cells.
 */

import type { SensorType, Metric, Unit } from './structure'

/** Raw sensor row from the API (numeric metric columns). */
export interface RawSensorData {
  id: number
  name: string
  type_id: number
  [key: `metric_${number}`]: number | null
}

/** One metric on a sensor with full metadata. */
export interface MetricValue {
  value: number
  metric: Metric
  unit: Unit
}

/** Sensor row after mapping structure (types, metric values). */
export interface Sensor {
  id: number
  name: string
  type: SensorType | null
  [key: `metric_${number}`]: MetricValue | undefined
}

/** Response body for POST /measurements (sensor rows). */
export interface SensorsResponse {
  data: RawSensorData[]
}
