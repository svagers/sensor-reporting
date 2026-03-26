import { markRaw } from 'vue'
import type { TableFilter } from '@/types/tableFilter'
import type { Sensor } from '@/types/sensor'
import NameSearchFilter from '@/components/app/filters/NameSearchFilter.vue'

export function applyNameSearch(rows: any[], value: unknown): any[] {
  if (value === undefined || value === null) return rows
  const q = String(value).trim().toLowerCase()
  if (!q) return rows
  return rows.filter((row: any) =>
    String(row?.name ?? '').toLowerCase().includes(q)
  )
}

export const nameSearchFilter: TableFilter<Sensor> = {
  component: markRaw(NameSearchFilter),
  apply: applyNameSearch,
}
