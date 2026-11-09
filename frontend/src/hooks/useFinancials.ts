import { useCallback, useEffect, useState } from 'react'
import * as FinancialsService from '../services/FinancialsService'
import { ApiError } from '../services/API'
import type { YearRange } from '../constants/yearRange'
import type { FilingStatements } from '../services/types/FinancialsTypes'

// Cached financial statements for every 10-K/10-Q in the range (newest first).
export function useFinancials(tckr: string, range: YearRange) {
  const [filings, setFilings] = useState<FilingStatements[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setFilings(await FinancialsService.getFinancials(tckr, range))
    } catch (err) {
      setFilings([])
      setError(err instanceof ApiError ? err.detail : 'Failed to load financial statements')
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- range is a fresh object each render; depend on its primitives instead
  }, [tckr, range.start, range.end])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches statements for the current tckr/range on mount and whenever they change
    refresh()
  }, [refresh])

  return { filings, error, loading, refresh }
}
