<template>
  <div>
    <div class="mb-3 flex justify-end">
      <ColumnControl :columns="columns" @columns-changed="onColumnsChanged" />
    </div>
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-200">
    <div class="overflow-auto max-h-[min(70vh,48rem)]">
      <table class="min-w-full border-separate border-spacing-0">
        <thead>
          <tr class="border-b border-gray-200">
            <th 
              v-for="(column, index) in visibleColumns" 
              :key="column.columnKey"
              :class="[
                'px-6 py-4 text-left align-bottom bg-gray-50',
                index === 0
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
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(row, rowIndex) in sortedData" 
            :key="rowIndex" 
            class="group border-b border-gray-100 hover:bg-gray-50 transition-colors"
          >
            <td 
              v-for="(column, colIndex) in visibleColumns" 
              :key="column.columnKey"
              :class="[
                'px-6 py-3',
                colIndex === 0
                  ? 'sticky left-0 z-10 bg-white shadow-[2px_0_8px_rgba(0,0,0,0.06)] group-hover:bg-gray-50'
                  : '',
              ]"
            >
              <component 
                :is="column.cellComponent"
                v-bind="column.cellProps"
                :data="row"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Column } from '@/types/column'
import ColumnControl from '@/components/ui/input/ColumnControl.vue'

interface Props {
  columns: Column[]
  data: any[]
}

const props = defineProps<Props>()

const selectedColumnKeys = ref<string[]>([])

function onColumnsChanged(keys: string[]) {
  selectedColumnKeys.value = keys
  console.log(selectedColumnKeys.value)
}

const visibleColumns = computed<Column[]>(() => {
  const keys = selectedColumnKeys.value
  if (keys.length === 0) return props.columns
  const allow = new Set(keys)
  return props.columns.filter((c) => allow.has(c.columnKey))
})

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

    // Handle null/undefined
    if (aValue == null) return 1
    if (bValue == null) return -1

    // String comparison
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return direction === 'asc' 
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }

    // Numeric comparison
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
