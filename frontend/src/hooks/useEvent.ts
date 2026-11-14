import { useEffect, useState } from 'react'
import * as EventsService from '../services/EventsService'
import { ApiError } from '../services/API'

// Markdown body of one 8-K, loaded when an event is selected.
export function useEvent(tckr: string, id: string | null) {
  // Stored with the id it was fetched for, so a previous event is never shown for the new selection.
  const [data, setData] = useState<{ id: string; markdown: string; error: string | null }>({ id: '', markdown: '', error: null })

  useEffect(() => {
    if (!id) return
    let cancelled = false
    EventsService.getEvent(tckr, id)
      .then((body) => !cancelled && setData({ id, markdown: body.markdown, error: null }))
      .catch((err) => !cancelled && setData({ id, markdown: '', error: err instanceof ApiError ? err.detail : 'Failed to load event' }))
    return () => { cancelled = true }
  }, [tckr, id])

  const current = data.id === id
  return { markdown: current ? data.markdown : '', error: current ? data.error : null, loading: !!id && !current }
}
