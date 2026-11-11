import { useCallback, useEffect, useRef, useState } from 'react'
import * as FinancialsService from '../services/FinancialsService'
import { ApiError } from '../services/API'
import type { YearRange } from '../constants/yearRange'
import type { FilingStatements } from '../services/types/FinancialsTypes'

// Cached financial statements for every 10-K/10-Q in the range (newest first).
export function useFinancials(tckr: string, range: YearRange) {
  const key = `${tckr}:${range.start}-${range.end}`
  // Data is stored with the key it was fetched for, so another ticker's statements are never shown.
  const [data, setData] = useState<{ key: string; filings: FilingStatements[] }>({ key: '', filings: [] })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const latest = useRef(0)

  const refresh = useCallback(async () => {
    const id = ++latest.current
    setLoading(true)
    setError(null)
    try {
      const filings = await FinancialsService.getFinancials(tckr, range)
      if (id === latest.current) setData({ key, filings })
    } catch (err) {
      if (id !== latest.current) return
      setData({ key, filings: [] })
      setError(err instanceof ApiError ? err.detail : 'Failed to load financial statements')
    } finally {
      if (id === latest.current) setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- range is a fresh object each render; key covers its primitives
  }, [key])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches statements for the current tckr/range on mount and whenever they change
    refresh()
  }, [refresh])

  const current = data.key === key
  // Not loaded until data for this ticker/range has arrived (avoids a false "empty" right after a switch).
  return { filings: current ? data.filings : [], error, loading: loading || !current, refresh }
}
