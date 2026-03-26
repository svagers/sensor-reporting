/**
 * Column definition types
 */

export interface Column {
  columnKey: string
  label: string
  /** When true, this column may be turned off in the column control. */
  disableable: boolean
  sortKey?: (row: any) => any
  headerComponent: any
  headerProps: Record<string, any>
  cellComponent?: any
  cellProps?: Record<string, any>
}
