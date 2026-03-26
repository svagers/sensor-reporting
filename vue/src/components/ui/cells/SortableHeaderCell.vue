<template>
  <div 
    class="flex items-end justify-between cursor-pointer select-none text-aranet-muted transition-colors text-sm hover:text-aranet-red"
    @click="emit('sort', columnKey)"
  >
    <slot></slot>
    
    <span v-if="is_ordered" class="ml-2 flex items-center text-aranet-red">
      <svg
        v-if="direction === 'asc'"
        xmlns="http://www.w3.org/2000/svg"
        class="h-3.5 w-3.5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
      </svg>
      <svg
        v-else
        xmlns="http://www.w3.org/2000/svg"
        class="h-3.5 w-3.5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  columnKey: string
  is_ordered: boolean
  direction: 'asc' | 'desc'
}

defineProps<Props>()

const emit = defineEmits<{
  sort: [columnKey: string]
}>()
</script>
