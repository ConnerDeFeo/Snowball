import { useCallback, useEffect, useState } from 'react'
import * as CompanyService from '../services/CompanyService'
import { ApiError } from '../services/API'
import type { YearRange } from '../constants/yearRange'
import type { GradedTimePeriod } from '../services/types/GradingTypes'

export function useGrades(tckr: string, range: YearRange) {
  const [serverGrades, setServerGrades] = useState<GradedTimePeriod[]>([])
  const [serverAvailable, setServerAvailable] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const grades = await CompanyService.getGrades(tckr, range)
      setServerGrades(grades)
      setServerAvailable(true)
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        setServerGrades([])
        setServerAvailable(false)
      } else {
        setServerGrades([])
        setError(err instanceof ApiError ? err.detail : 'Failed to load grades')
      }
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- range is a fresh object each render; depend on its primitives instead
  }, [tckr, range.start, range.end])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches grades for the current tckr/range on mount and whenever they change
    refresh()
  }, [refresh])

  return { serverGrades, serverAvailable, error, loading, refresh }
}
