/**
 * Toast service bridge — `registerToastService` is called from App.vue; `showErrorToast` from api.ts and elsewhere.
 */

import type { ToastMessageOptions } from 'primevue/toast'
import type { ToastServiceMethods } from 'primevue/toastservice'

let toastService: ToastServiceMethods | null = null

export function registerToastService(service: ToastServiceMethods): void {
  toastService = service
}

export function showErrorToast(
  summary: string,
  detail?: string,
  life = 6000
): void {
  toastService?.add({
    severity: 'error',
    summary,
    detail,
    life,
    closable: true,
  } satisfies ToastMessageOptions)
}
