/**
 * Sensor Data Mapper
 * Transforms raw API data into enriched Sensor objects
 */

import type { RawSensorData, Sensor } from '@/types/measurement'
import { getSensorTypeById, getMetricById } from '@/stores/structure'

/**
 * Transform raw sensor data into enriched Sensor object
 * Maps type_id to SensorType and transforms metric_X properties to MetricValue objects
 */
export function mapRawSensorToSensor(rawSensor: RawSensorData): Sensor {
  const sensorType = getSensorTypeById(rawSensor.type_id)
  
  const sensor: Sensor = {
    id: rawSensor.id,
    name: rawSensor.name,
    type: sensorType || null,
  }
  
  // Transform all metric_X properties
  for (const key in rawSensor) {
    const match = key.match(/^metric_(\d+)$/)
    if (match) {
      const metricId = parseInt(match[1], 10)
      const value = rawSensor[key as keyof RawSensorData]
      
      if (value !== null && value !== undefined) {
        const metric = getMetricById(metricId)
        
        if (metric) {
          sensor[key as `metric_${number}`] = {
            value: value as number,
            metric,
            unit: metric.primary_unit,
          }
        }
      }
    }
  }
  
  return sensor
}

/**
 * Transform array of raw sensors into enriched Sensor objects
 */
export function mapRawSensorsToSensors(rawSensors: RawSensorData[]): Sensor[] {
  return rawSensors.map(mapRawSensorToSensor)
}
