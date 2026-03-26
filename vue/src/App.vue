<template>
  <OverlayError
    v-if="apiUnreachable"
    title="Can't reach the API"
    description="The server didn't respond. Check that the API is running, your network connection, and that the configured API URL is correct."
  />
  <BlockUI
    v-else
    :blocked="structureLoading"
    :fullScreen="true"
    class="flex min-h-0 min-w-0 flex-1 flex-col"
  >
    <template #default>
      <div
        class="box-border flex min-h-0 w-full flex-1 flex-col px-4 py-12 sm:px-6 lg:px-8"
      >
        <DataTable v-if="structure" :provider="sensors" />
      </div>
    </template>
  </BlockUI>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { loadStructure, structureLoading, structure } from '@/stores/structure'
import { apiUnreachable } from '@/stores/connection'
import { useSensors } from '@/composables/useSensors'
import OverlayError from '@/components/app/OverlayError.vue'
import DataTable from '@/components/app/DataTable.vue'
import BlockUI from 'primevue/blockui'

const sensors = useSensors()

onMounted(() => {
  loadStructure()
})
</script>
