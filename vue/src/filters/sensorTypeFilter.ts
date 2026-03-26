import { markRaw } from 'vue'
import type { TableFilter } from '@/types/tableFilter'
import type { Sensor } from '@/types/sensor'
import SensorTypeFilter from '@/components/app/filters/SensorTypeFilter.vue'

export function applySensorType(rows: any[], value: unknown): any[] {
  if (value === undefined) return rows
  if (value === null) return rows.filter((row: any) => row?.type == null)
  const id = typeof value === 'number' ? value : Number(value)
  if (Number.isNaN(id)) return rows
  return rows.filter((row: any) => row?.type?.id === id)
}

export const sensorTypeFilter: TableFilter<Sensor> = {
  component: markRaw(SensorTypeFilter),
  apply: applySensorType,
}
