import { useCallback, useEffect, useState } from 'react'
import * as ChecklistService from '../services/ChecklistService'
import type { Category } from '../services/types/ChecklistTypes'

export function useChecklist() {
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setCategories(await ChecklistService.getChecklist())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load checklist')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches the checklist on mount
    refresh()
  }, [refresh])

  return { categories, loading, error, refresh }
}
