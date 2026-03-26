<template>
  <div v-if="metricValue" class="text-gray-900 font-mono">
    {{ metricValue.value.toFixed(metricValue.unit.precision) }}
  </div>
  <div v-else class="text-gray-400">
    -
  </div>
</template>

<script setup lang="ts">
import type { Sensor, MetricValue } from '@/types/measurement'
import { computed } from 'vue'

interface Props {
  data: Sensor
  metricKey: string
}

const props = defineProps<Props>()

const metricValue = computed(() => {
  return props.data[props.metricKey as keyof Sensor] as MetricValue | undefined
})
</script>
