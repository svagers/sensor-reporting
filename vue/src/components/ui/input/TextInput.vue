<template>
  <input
    :type="type"
    :value="text ?? ''"
    autocomplete="off"
    :placeholder="placeholder"
    :aria-label="ariaLabel"
    class="h-9 min-w-[12rem] w-full rounded-lg border border-gray-300 bg-white px-3 text-sm text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-200"
    @keyup="onKeyup"
  />
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    /** Current text shown in the field (controlled). */
    text?: string
    type?: string
    placeholder?: string
    ariaLabel?: string
  }>(),
  {
    type: 'text',
  }
)

const emit = defineEmits<{
  changed: [value: string]
}>()

function onKeyup(e: KeyboardEvent) {
  emit('changed', (e.target as HTMLInputElement).value)
}
</script>
