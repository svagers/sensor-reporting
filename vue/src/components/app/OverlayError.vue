<template>
  <div
    class="fixed inset-0 z-[9999] flex items-center justify-center bg-aranet-page px-6"
    role="alert"
    aria-live="assertive"
  >
    <div class="flex max-w-md flex-col items-center text-center">
      <div
        class="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-aranet-red/10 text-aranet-red"
        aria-hidden="true"
      >
        <svg
          class="h-9 w-9"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
          />
        </svg>
      </div>
      <h1 class="mb-3 text-xl font-semibold tracking-tight text-aranet-ink">
        {{ title }}
      </h1>
      <p class="mb-8 text-sm leading-relaxed text-aranet-muted">
        {{ description }}
      </p>
      <button
        type="button"
        class="rounded-full border border-aranet-border bg-aranet-white px-6 py-2.5 text-sm font-medium text-aranet-ink shadow-[0_2px_5px_rgba(29,29,29,0.08)] transition hover:bg-aranet-surface focus:outline-none focus:ring-2 focus:ring-aranet-red/25"
        @click="retry"
      >
        Try again
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()

function retry(): void {
  window.location.reload()
}
</script>
