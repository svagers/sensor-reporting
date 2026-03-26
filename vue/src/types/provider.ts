/**
 * Generic Data Provider Interface
 * Any composable that wants to work with DataTable must implement this interface
 */

import type { Ref, DeepReadonly } from 'vue'
import type { Column } from './column'

export interface DataProvider<T = any, F = any> {
  data: DeepReadonly<Ref<T[]>>
  isLoading: DeepReadonly<Ref<boolean>>
  error: DeepReadonly<Ref<Error | null>>
  currentFilters: DeepReadonly<Ref<F>>
  fetch: (filters?: F) => Promise<void>
  refresh: () => Promise<void>
  clear: () => void
  getColumns: () => Column[]
}
