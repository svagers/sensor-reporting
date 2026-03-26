<template>
  <div ref="rootRef" class="relative inline-flex">
    <button
      type="button"
      class="inline-flex h-9 min-w-[14rem] max-w-md items-center gap-2 rounded-lg border px-3 text-left text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-gray-200"
      :class="
        open
          ? 'border-gray-400 bg-gray-50 text-gray-900'
          : 'border-gray-300 bg-white text-gray-900 hover:border-gray-400 hover:bg-gray-50'
      "
      aria-haspopup="listbox"
      :aria-expanded="open"
      :aria-label="`Sensor type: ${selectedLabel}. Open list`"
      @click.stop="open = !open"
    >
      <span class="inline-flex shrink-0 items-center gap-2 text-gray-600" aria-hidden="true">
        <svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
          />
        </svg>
      </span>
      <span class="min-w-0 flex-1 truncate whitespace-nowrap">{{ selectedLabel }}</span>
      <svg
        class="h-4 w-4 shrink-0 text-gray-500 transition-transform"
        :class="{ 'rotate-180': open }"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        aria-hidden="true"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <div
      v-show="open"
      class="absolute left-0 top-full z-50 mt-1 w-[min(calc(100vw-2rem),22rem)] rounded-lg border border-gray-200 bg-white shadow-lg ring-1 ring-black/5"
      role="listbox"
    >
      <div class="max-h-[min(50vh,16rem)] overflow-y-auto overflow-x-auto py-1">
        <button
          type="button"
          role="option"
          class="flex w-full min-w-0 cursor-pointer items-center gap-3 px-3 py-2 text-left text-sm text-gray-800 transition-colors hover:bg-gray-50 focus:outline-none"
          :aria-selected="selectedTypeId === undefined"
          @click.stop="selectType(undefined)"
        >
          <svg
            v-if="selectedTypeId === undefined"
            class="h-5 w-5 shrink-0 text-emerald-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg
            v-else
            class="h-5 w-5 shrink-0 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <rect x="4" y="4" width="16" height="16" rx="2" stroke-width="2" />
          </svg>
          <span class="whitespace-nowrap">All types</span>
        </button>

        <button
          type="button"
          role="option"
          class="flex w-full min-w-0 cursor-pointer items-center gap-3 px-3 py-2 text-left text-sm text-gray-800 transition-colors hover:bg-gray-50 focus:outline-none"
          :aria-selected="selectedTypeId === null"
          @click.stop="selectType(null)"
        >
          <svg
            v-if="selectedTypeId === null"
            class="h-5 w-5 shrink-0 text-emerald-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg
            v-else
            class="h-5 w-5 shrink-0 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <rect x="4" y="4" width="16" height="16" rx="2" stroke-width="2" />
          </svg>
          <span class="whitespace-nowrap">No type</span>
        </button>

        <button
          v-for="st in allTypes"
          :key="st.id"
          type="button"
          role="option"
          class="flex w-full min-w-0 cursor-pointer items-center gap-3 px-3 py-2 text-left text-sm text-gray-800 transition-colors hover:bg-gray-50 focus:outline-none"
          :aria-selected="selectedTypeId === st.id"
          @click.stop="selectType(st.id)"
        >
          <svg
            v-if="selectedTypeId === st.id"
            class="h-5 w-5 shrink-0 text-emerald-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg
            v-else
            class="h-5 w-5 shrink-0 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <rect x="4" y="4" width="16" height="16" rx="2" stroke-width="2" />
          </svg>
          <span class="whitespace-nowrap">{{ st.name }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { structure } from '@/stores/structure'

const emit = defineEmits<{
  filterChanged: [value: number | undefined | null]
}>()

const open = ref(false)
const rootRef = ref<HTMLElement | null>(null)
const selectedTypeId = ref<number | undefined | null>(undefined)
const allTypes = computed(() => structure.value?.sensor_types ?? [])

const selectedLabel = computed(() => {
  if (selectedTypeId.value === undefined) return 'All types'
  if (selectedTypeId.value === null) return 'No type'
  const t = allTypes.value.find((x) => x.id === selectedTypeId.value)
  return t?.name ?? 'All types'
})

function selectType(id: number | undefined | null) {
  selectedTypeId.value = id
  emit('filterChanged', id)
  open.value = false
}

function onDocumentPointerDown(e: MouseEvent | PointerEvent) {
  const el = rootRef.value
  if (!el || !open.value) return
  const target = e.target as Node
  if (!el.contains(target)) {
    open.value = false
  }
}

onMounted(() => {
  document.addEventListener('pointerdown', onDocumentPointerDown, true)
})

onUnmounted(() => {
  document.removeEventListener('pointerdown', onDocumentPointerDown, true)
})
</script>
