<template>
  <BlockUI :blocked="provider.isLoading.value">
    <template #default>
      <div v-if="!provider.isLoading.value && provider.data.value.length > 0">
        <div class="mb-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-2">Sensor Measurements</h2>
          <p class="text-gray-600">{{ provider.data.value.length }} sensors found</p>
        </div>
        
        <Table 
          :columns="provider.getColumns()" 
          :data="provider.data.value"
        />
      </div>
      <div v-else-if="!provider.isLoading.value" class="text-center py-12">
        <p class="text-gray-600 text-lg">No data available</p>
      </div>
    </template>
  </BlockUI>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import type { DataProvider } from '@/types/provider'
import BlockUI from 'primevue/blockui'
import Table from '@/components/ui/Table.vue'

interface Props {
  provider: DataProvider
}

const props = defineProps<Props>()

onMounted(() => {
  props.provider.fetch()
})
</script>
