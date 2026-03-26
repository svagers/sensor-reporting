/**
 * Column definition types
 */

export interface Column {
  columnKey: string
  sortKey?: (row: any) => any
  headerComponent: any
  headerProps: Record<string, any>
  cellComponent?: any
  cellProps?: Record<string, any>
}
