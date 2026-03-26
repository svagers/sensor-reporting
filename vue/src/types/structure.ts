/**
 * Structure types for global application data
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

export interface StructureData {
  sensor_types: SensorType[]
  metrics: Metric[]
}
