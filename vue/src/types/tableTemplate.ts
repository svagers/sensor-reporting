import type { Column } from './column'
import type { TableFilter } from './tableFilter'

/** Column layout + optional filters for a table view */
export interface TableTemplate<T = unknown> {
  getColumns: () => Column[]
  getFilters?: () => Record<string, TableFilter<T>>
}
