<template>
  <div class="flex items-center gap-2">
    <TextInput
      type="search"
      :text="searchText"
      placeholder="Search name…"
      aria-label="Search by sensor name"
      @changed="onInputChanged"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TextInput from '@/components/ui/input/TextInput.vue'

const searchText = ref('')

const emit = defineEmits<{
  filterChanged: [value: string | undefined]
}>()

function onInputChanged(value: string) {
  searchText.value = value
  const trimmed = value.trim()
  emit('filterChanged', trimmed === '' ? undefined : trimmed)
}
</script>
