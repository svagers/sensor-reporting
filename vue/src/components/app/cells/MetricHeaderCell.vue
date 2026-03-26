<template>
  <SortableHeaderCell 
    :columnKey="`metric_${metric.id}`" 
    :is_ordered="is_ordered" 
    :direction="direction"
  >
    <div class="flex flex-col gap-0.5">
      <span class="text-xs text-gray-500 font-normal leading-tight">{{ metric.primary_unit.name }}</span>
      <span class="text-sm font-semibold leading-tight">{{ metric.name }}</span>
    </div>
  </SortableHeaderCell>
</template>

<script setup lang="ts">
import type { Metric } from '@/types/structure'
import SortableHeaderCell from '@/components/ui/cells/SortableHeaderCell.vue'

interface Props {
  metric: Metric
  is_ordered: boolean
  direction: 'asc' | 'desc'
}

defineProps<Props>()
</script>
