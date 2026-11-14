import { useCallback, useEffect, useRef, useState } from 'react'
import * as EventsService from '../services/EventsService'
import { ApiError } from '../services/API'
import type { YearRange } from '../constants/yearRange'
import type { EventMeta } from '../services/types/EventsTypes'

// Cached 8-K metadata for the range (newest first).
export function useEvents(tckr: string, range: YearRange) {
  const key = `${tckr}:${range.start}-${range.end}`
  // Data is stored with the key it was fetched for, so another ticker's events are never shown.
  const [data, setData] = useState<{ key: string; events: EventMeta[] }>({ key: '', events: [] })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const latest = useRef(0)

  const refresh = useCallback(async () => {
    const id = ++latest.current
    setLoading(true)
    setError(null)
    try {
      const events = await EventsService.getEvents(tckr, range)
      if (id === latest.current) setData({ key, events })
    } catch (err) {
      if (id !== latest.current) return
      setData({ key, events: [] })
      setError(err instanceof ApiError ? err.detail : 'Failed to load events')
    } finally {
      if (id === latest.current) setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- range is a fresh object each render; key covers its primitives
  }, [key])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches events for the current tckr/range on mount and whenever they change
    refresh()
  }, [refresh])

  const current = data.key === key
  return { events: current ? data.events : [], error, loading: loading || !current, refresh }
}
