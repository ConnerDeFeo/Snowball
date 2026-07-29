import { useCallback, useEffect, useState } from 'react'
import * as RubricService from '../services/RubricService'
import type { RubricCategory } from '../enums/RubricCategory'
import type { RubricShape } from '../services/types/RubricTypes'

export function useRubric() {
  const [shapes, setShapes] = useState<Map<RubricCategory, RubricShape>>(new Map())
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const list = await RubricService.getRubric()
      const map = new Map<RubricCategory, RubricShape>()
      for (const shape of list) map.set(shape.rubric_category, shape)
      setShapes(map)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load rubric')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches the rubric list on mount
    refresh()
  }, [refresh])

  return { shapes, loading, error, refresh }
}
