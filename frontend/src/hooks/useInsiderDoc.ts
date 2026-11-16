import { useEffect, useState } from 'react'
import * as InsidersService from '../services/InsidersService'
import { ApiError } from '../services/API'

// Markdown body of one insider filing, loaded when it is selected.
export function useInsiderDoc(tckr: string, id: string | null) {
  // Stored with the id it was fetched for, so a previous filing is never shown for the new selection.
  const [data, setData] = useState<{ id: string; markdown: string; error: string | null }>({ id: '', markdown: '', error: null })

  useEffect(() => {
    if (!id) return
    let cancelled = false
    InsidersService.getInsiderDoc(tckr, id)
      .then((body) => !cancelled && setData({ id, markdown: body.markdown, error: null }))
      .catch((err) => !cancelled && setData({ id, markdown: '', error: err instanceof ApiError ? err.detail : 'Failed to load filing' }))
    return () => { cancelled = true }
  }, [tckr, id])

  const current = data.id === id
  return { markdown: current ? data.markdown : '', error: current ? data.error : null, loading: !!id && !current }
}
