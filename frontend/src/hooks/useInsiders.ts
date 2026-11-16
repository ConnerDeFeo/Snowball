import { useCallback, useEffect, useRef, useState } from 'react'
import * as InsidersService from '../services/InsidersService'
import { ApiError } from '../services/API'
import type { YearRange } from '../constants/yearRange'
import type { InsiderFiling } from '../services/types/InsidersTypes'

// Cached insider filings (Form 4, 13D) for the range, newest first.
export function useInsiders(tckr: string, range: YearRange) {
  const key = `${tckr}:${range.start}-${range.end}`
  // Data is stored with the key it was fetched for, so another ticker's filings are never shown.
  const [data, setData] = useState<{ key: string; filings: InsiderFiling[] }>({ key: '', filings: [] })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const latest = useRef(0)

  const refresh = useCallback(async () => {
    const id = ++latest.current
    setLoading(true)
    setError(null)
    try {
      const filings = await InsidersService.getInsiders(tckr, range)
      if (id === latest.current) setData({ key, filings })
    } catch (err) {
      if (id !== latest.current) return
      setData({ key, filings: [] })
      setError(err instanceof ApiError ? err.detail : 'Failed to load insider filings')
    } finally {
      if (id === latest.current) setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- range is a fresh object each render; key covers its primitives
  }, [key])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches filings for the current tckr/range on mount and whenever they change
    refresh()
  }, [refresh])

  const current = data.key === key
  return { filings: current ? data.filings : [], error, loading: loading || !current, refresh }
}
