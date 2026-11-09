import { useCallback, useEffect, useState } from 'react'
import * as EvidenceService from '../services/EvidenceService'
import { ApiError } from '../services/API'
import type { YearRange } from '../constants/yearRange'
import type { EvidenceCategory } from '../services/types/EvidenceTypes'

// Stored evidence for the whole checklist (no Bedrock call on the backend).
export function useEvidence(tckr: string, range: YearRange) {
  const [serverEvidence, setServerEvidence] = useState<EvidenceCategory[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setServerEvidence(await EvidenceService.getEvidence(tckr, range))
    } catch (err) {
      setServerEvidence([])
      setError(err instanceof ApiError ? err.detail : 'Failed to load evidence')
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- range is a fresh object each render; depend on its primitives instead
  }, [tckr, range.start, range.end])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches evidence for the current tckr/range on mount and whenever they change
    refresh()
  }, [refresh])

  return { serverEvidence, error, loading, refresh }
}
