<template>
  <div class="flex flex-col whitespace-nowrap">
    <div class="flex items-center gap-1">
      <svg 
        v-if="!data.name || data.name.trim() === ''"
        xmlns="http://www.w3.org/2000/svg" 
        class="h-4 w-4 text-amber-500" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span 
        :class="[
          'font-medium',
          !data.name || data.name.trim() === '' ? 'text-amber-600 italic' : 'text-gray-900'
        ]"
      >
        {{ data.name && data.name.trim() !== '' ? data.name : 'Unnamed sensor' }}
      </span>
    </div>
    
    <div class="flex items-center gap-1">
      <svg 
        v-if="!data.type"
        xmlns="http://www.w3.org/2000/svg" 
        class="h-3 w-3 text-amber-500" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span 
        :class="[
          'text-xs',
          !data.type ? 'text-amber-600 italic' : 'text-gray-500'
        ]"
      >
        {{ data.type ? data.type.name : 'Missing type' }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Sensor } from '@/types/measurement'

interface Props {
  data: Sensor
}

defineProps<Props>()
</script>
