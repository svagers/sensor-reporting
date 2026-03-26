<template>
  <div
    class="flex min-h-0 min-w-0 w-full flex-1 flex-col overflow-hidden rounded-2xl border border-aranet-border bg-aranet-white shadow-aranet"
  >
    <div class="min-h-0 min-w-0 flex-1 overflow-auto overscroll-contain">
      <table class="min-w-full border-separate border-spacing-0">
        <thead>
          <tr class="border-b border-aranet-border">
            <template v-for="column in columns" :key="column.columnKey">
              <th
                v-if="isColumnVisible(column.columnKey)"
                :class="[
                  'px-6 py-4 text-left align-bottom bg-aranet-surface',
                  column.columnKey === columns[0]?.columnKey
                    ? 'sticky left-0 top-0 z-30 shadow-[2px_0_8px_rgba(0,0,0,0.06)]'
                    : 'sticky top-0 z-20',
                ]"
              >
                <component 
                  :is="column.headerComponent"
                  v-bind="column.headerProps"
                  :is_ordered="currentSort?.columnKey === column.columnKey"
                  :direction="currentSort?.direction || 'desc'"
                  @sort="handleSort"
                />
              </th>
            </template>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(row, rowIndex) in sortedData" 
            :key="rowIndex" 
            class="group border-b border-aranet-border/60 transition-colors hover:bg-aranet-surface"
          >
            <template v-for="column in columns" :key="column.columnKey">
              <td
                v-if="isColumnVisible(column.columnKey)"
                :class="[
                  'px-6 py-3',
                  column.columnKey === columns[0]?.columnKey
                    ? 'sticky left-0 z-10 bg-aranet-white shadow-[2px_0_8px_rgba(0,0,0,0.06)] group-hover:bg-aranet-surface'
                    : '',
                ]"
              >
                <component 
                  :is="column.cellComponent"
                  v-bind="column.cellProps"
                  :data="row"
                />
              </td>
            </template>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Column } from '@/types/column'

interface Props {
  columns: Column[]
  visibleColumnKeys: string[]
  data: readonly any[]
}

const props = defineProps<Props>()

function isColumnVisible(columnKey: string): boolean {
  const keys = props.visibleColumnKeys
  if (keys.length === 0) return true
  return keys.includes(columnKey)
}

interface SortState {
  columnKey: string
  direction: 'asc' | 'desc'
}

const currentSort = ref<SortState | null>(null)

const sortedData = computed(() => {
  if (!currentSort.value) {
    return props.data
  }

  const { columnKey, direction } = currentSort.value
  const column = props.columns.find(c => c.columnKey === columnKey)
  
  if (!column?.sortKey) {
    return props.data
  }
  
  return [...props.data].sort((a, b) => {
    const aValue = column.sortKey!(a)
    const bValue = column.sortKey!(b)

    if (aValue == null) return 1
    if (bValue == null) return -1

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return direction === 'asc' 
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }

    if (aValue < bValue) return direction === 'asc' ? -1 : 1
    if (aValue > bValue) return direction === 'asc' ? 1 : -1
    return 0
  })
})

const handleSort = (columnKey: string) => {
  if (currentSort.value?.columnKey === columnKey) {
    currentSort.value.direction = currentSort.value.direction === 'asc' ? 'desc' : 'asc'
  } else {
    currentSort.value = {
      columnKey,
      direction: 'desc',
    }
  }
}
</script>
