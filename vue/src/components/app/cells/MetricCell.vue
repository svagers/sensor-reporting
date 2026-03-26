<template>
  <div v-if="metricValue" class="font-mono text-aranet-ink">
    {{ metricValue.value.toFixed(metricValue.unit.precision) }}
  </div>
  <div v-else class="text-aranet-faint">
    -
  </div>
</template>

<script setup lang="ts">
import type { Sensor, MetricValue } from '@/types/sensor'
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
