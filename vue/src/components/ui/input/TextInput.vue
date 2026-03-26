<template>
  <input
    :type="type"
    :value="text ?? ''"
    autocomplete="off"
    :placeholder="placeholder"
    :aria-label="ariaLabel"
    class="h-9 min-w-[12rem] w-full rounded border border-aranet-border bg-aranet-white px-3 text-sm text-aranet-ink shadow-[0_2px_5px_rgba(29,29,29,0.08)] placeholder:text-aranet-faint focus:border-aranet-muted focus:outline-none focus:ring-2 focus:ring-aranet-red/20"
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
