<template>
  <BlockUI :blocked="structureLoading" :fullScreen="true" class="min-h-screen">
    <template #default>
      <div class="min-h-screen">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div class="text-center mb-12">
            <h1 class="text-5xl font-bold text-gray-900 mb-4">Saftehnika</h1>
            <p class="text-gray-600 text-lg">Sensor Data Management Platform</p>
          </div>
          
          <DataTable v-if="structure" :provider="measurements" />
        </div>
      </div>
    </template>
  </BlockUI>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { loadStructure, structureLoading, structure } from '@/stores/structure'
import { useMeasurements } from '@/composables/useMeasurements'
import DataTable from '@/components/app/DataTable.vue'
import BlockUI from 'primevue/blockui'

const measurements = useMeasurements()

onMounted(() => {
  loadStructure()
})
</script>
