/**
 * App-wide connection state — set when fetch fails before any HTTP response (unreachable API).
 */

import { ref, readonly } from 'vue'

const unreachable = ref(false)

export function markApiUnreachable(): void {
  unreachable.value = true
}

export function markApiReachable(): void {
  unreachable.value = false
}

export const apiUnreachable = readonly(unreachable)
