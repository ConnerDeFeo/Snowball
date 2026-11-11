import { useEffect, useRef } from 'react'

interface Options {
  enabled: boolean
  empty: boolean
  busy: boolean
  fetch: () => void
  key: string
}

// Starts a filings fetch once per key when a view is enabled but has nothing to show.
// The once-per-key guard stops a loop when a fetch still leaves it empty.
export function useAutoFetchFilings({ enabled, empty, busy, fetch, key }: Options) {
  const tried = useRef(new Set<string>())

  useEffect(() => {
    if (!enabled || !empty || busy || tried.current.has(key)) return
    tried.current.add(key)
    fetch()
  }, [enabled, empty, busy, fetch, key])
}
