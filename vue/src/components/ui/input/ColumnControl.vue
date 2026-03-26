<template>
  <div ref="rootRef" class="relative inline-flex">
    <button
      type="button"
      class="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border shadow-sm transition focus:outline-none"
      :class="
        open
          ? 'border-aranet-muted bg-aranet-surface text-aranet-ink'
          : 'border-aranet-border bg-aranet-white text-aranet-muted hover:border-aranet-muted hover:bg-aranet-surface'
      "
      :aria-expanded="open"
      aria-haspopup="listbox"
      aria-label="Column visibility"
      @click.stop="open = !open"
    >
      <svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M4 4h4v16H4V4zm6 0h4v16h-4V4zm6 0h4v16h-4V4z" />
      </svg>
    </button>

    <div
      v-show="open"
      class="absolute right-0 top-full z-50 mt-1 min-w-[14rem] rounded-lg border border-aranet-border bg-aranet-white py-1 shadow-aranet ring-1 ring-black/5"
      role="listbox"
    >
      <template v-for="col in columns" :key="col.columnKey">
        <button
          v-if="col.disableable"
          type="button"
          class="flex w-full cursor-pointer items-center gap-3 whitespace-nowrap px-3 py-2 text-left text-sm text-aranet-ink transition-colors hover:bg-aranet-surface focus:outline-none"
          role="option"
          :aria-selected="isVisible(col.columnKey)"
          @click.stop="toggle(col.columnKey)"
        >
          <svg
            v-if="isVisible(col.columnKey)"
            class="h-5 w-5 shrink-0 text-aranet-green"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
          <svg
            v-else
            class="h-5 w-5 shrink-0 text-aranet-faint"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
          </svg>
          <span class="whitespace-nowrap">{{ col.label }}</span>
        </button>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { Column } from '@/types/column'

const props = defineProps<{
  columns: Column[]
}>()

const emit = defineEmits<{
  columnsChanged: [visibleColumnKeys: string[]]
}>()

const visibleColumnKeys = ref<string[]>(props.columns.map((c) => c.columnKey))
const open = ref(false)
const rootRef = ref<HTMLElement | null>(null)

onMounted(() => {
  emit('columnsChanged', visibleColumnKeys.value)
  document.addEventListener('pointerdown', onDocumentPointerDown, true)
})

onUnmounted(() => {
  document.removeEventListener('pointerdown', onDocumentPointerDown, true)
})

const isVisible = (columnKey: string) =>
  visibleColumnKeys.value.includes(columnKey)

const toggle = (columnKey: string) => {
  const next = new Set(visibleColumnKeys.value)
  if (next.has(columnKey)) next.delete(columnKey)
  else next.add(columnKey)
  visibleColumnKeys.value = [...next]
  emit('columnsChanged', visibleColumnKeys.value)
}

const onDocumentPointerDown = (e: MouseEvent | PointerEvent) => {
  const el = rootRef.value
  if (!el || !open.value) return
  const target = e.target as Node
  if (!el.contains(target)) {
    open.value = false
  }
}
</script>
