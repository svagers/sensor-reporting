<template>
  <BlockUI
    :blocked="provider.isLoading.value"
    class="flex min-h-0 min-w-0 flex-1 flex-col"
  >
    <template #default>
      <div
        v-if="!provider.isLoading.value && provider.data.value.length > 0"
        class="flex min-h-0 w-full min-w-0 flex-1 flex-col"
      >
        <div class="mb-6 shrink-0">
          <h2 class="text-2xl font-semibold tracking-tight text-aranet-ink">Sensor Readings</h2>
        </div>

        <div class="mb-3 flex shrink-0 flex-wrap items-center justify-between gap-3">
          <div class="flex flex-wrap items-center gap-3">
            <component
              :is="filter.component"
              v-for="(filter, filterId) in filters"
              :key="filterId"
              @filter-changed="(v: unknown) => onFilterChanged(filterId, v)"
            />
          </div>
          <ColumnControl
            :columns="columns"
            @columns-changed="onColumnsChanged"
          />
        </div>

        <div class="flex min-h-0 min-w-0 w-full flex-1 flex-col">
          <Table
            :columns="columns"
            :visible-column-keys="visibleColumnKeys"
            :data="filteredData"
          />
        </div>

        <p class="mt-2 shrink-0 text-xs text-aranet-faint">
          {{ filteredData.length }} of {{ totalSensorCount }} sensors
        </p>
      </div>
      <div v-else-if="!provider.isLoading.value" class="text-center py-12">
        <p class="text-lg text-aranet-muted">No data available</p>
      </div>
    </template>
  </BlockUI>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import type { DataProvider } from '@/types/provider'
import type { Sensor } from '@/types/sensor'
import type { TableFilter } from '@/types/tableFilter'
import BlockUI from 'primevue/blockui'
import Table from '@/components/ui/Table.vue'
import ColumnControl from '@/components/ui/input/ColumnControl.vue'

interface Props {
  provider: DataProvider<Sensor>
}

const props = defineProps<Props>()
const filterValues = reactive<Record<string, unknown>>({})
const visibleColumnKeys = ref<string[]>([])
const columns = props.provider.tableTemplate.getColumns()
const filters = props.provider.tableTemplate.getFilters?.() ?? ({} as Record<string, TableFilter<Sensor>>)

const totalSensorCount = computed(() => props.provider.data.value.length)

const filteredData = computed(() => {
  let rows: Sensor[] = [...props.provider.data.value] as Sensor[]

  for (const [filterId, f] of Object.entries(filters)) {
    rows = f.apply(rows, filterValues[filterId])
  }

  return rows
})

function onColumnsChanged(keys: string[]) {
  visibleColumnKeys.value = keys
}

function onFilterChanged(filterId: string, value: unknown) {
  filterValues[filterId] = value
}

onMounted(() => {
  props.provider.fetch()
})
</script>
