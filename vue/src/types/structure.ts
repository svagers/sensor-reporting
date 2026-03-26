/**
 * Structure domain types (units, metrics, sensor types).
 */

export interface Unit {
  id: number
  name: string
  precision: number
}

export interface Metric {
  id: number
  name: string
  primary_unit: Unit
}

export interface SensorType {
  id: number
  type_id: number
  variant_id: number
  name: string
}
