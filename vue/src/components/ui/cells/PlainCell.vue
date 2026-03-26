<template>
  <div>
    {{ getValue() }}
  </div>
</template>

<script setup lang="ts">
interface Props {
  data: Record<string, any>
  cellKey: string
}

const props = defineProps<Props>()

const getValue = () => {
  const keys = props.cellKey.split('.')
  let value: any = props.data
  
  for (const key of keys) {
    if (value && typeof value === 'object') {
      value = value[key]
    } else {
      return '-'
    }
  }
  
  return value !== undefined && value !== null ? value : '-'
}
</script>
