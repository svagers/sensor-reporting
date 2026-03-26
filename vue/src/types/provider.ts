/**
 * Generic Data Provider Interface
 * Any composable that wants to work with DataTable must implement this interface
 */

import type { Ref, DeepReadonly } from 'vue'
import type { TableTemplate } from './tableTemplate'

export interface DataProvider<T = any> {
  data: DeepReadonly<Ref<T[]>>
  isLoading: DeepReadonly<Ref<boolean>>
  error: DeepReadonly<Ref<Error | null>>
  fetch: () => Promise<void>
  refresh: () => Promise<void>
  clear: () => void
  tableTemplate: TableTemplate<T>
}
