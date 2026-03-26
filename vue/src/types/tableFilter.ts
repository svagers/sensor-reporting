import type { Component } from 'vue'

export interface TableFilter<T = unknown> {
  component: Component
  apply: (rows: T[], value: unknown) => T[]
}
