<template>
  <SortableHeaderCell 
    :columnKey="columnKey" 
    :is_ordered="is_ordered" 
    :direction="direction"
  >
    <span class="text-sm">{{ label }}</span>
  </SortableHeaderCell>
</template>

<script setup lang="ts">
import SortableHeaderCell from './SortableHeaderCell.vue'

interface Props {
  label: string
  columnKey: string
  is_ordered: boolean
  direction: 'asc' | 'desc'
}

defineProps<Props>()
</script>
