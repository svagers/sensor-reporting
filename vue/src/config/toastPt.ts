import type { ToastPassThroughOptions } from 'primevue/toast'

/**
 * PrimeVue Toast passthrough — matches app design tokens (aranet.*, shadow-aranet, font-sans).
 */
export const toastPt = {
  root: {
    class: 'w-full max-w-sm gap-0 p-4 font-sans sm:p-6',
  },
  message: {
    class:
      'pointer-events-auto mb-0 min-w-0 overflow-hidden rounded-2xl border border-aranet-border border-l-4 border-l-aranet-red bg-aranet-white shadow-aranet ring-1 ring-black/5',
  },
  messageContent: {
    class: 'flex items-start gap-3 p-4',
  },
  messageIcon: {
    class: 'mt-0.5 h-6 w-6 shrink-0 text-aranet-red',
  },
  messageText: {
    class: 'flex min-w-0 flex-1 flex-col gap-1 text-left',
  },
  summary: {
    class: 'text-sm font-semibold tracking-tight text-aranet-ink',
  },
  detail: {
    class: 'break-words text-xs leading-relaxed text-aranet-muted',
  },
  buttonContainer: {
    class: 'ml-1 shrink-0 self-start',
  },
  closeButton: {
    class:
      '-m-1 rounded-lg p-1.5 text-aranet-faint ring-0 outline-none transition-colors hover:bg-aranet-surface hover:text-aranet-ink focus:outline-none focus:ring-0 focus-visible:outline-none focus-visible:ring-0',
  },
  closeIcon: {
    class: 'h-4 w-4',
  },
} satisfies ToastPassThroughOptions
