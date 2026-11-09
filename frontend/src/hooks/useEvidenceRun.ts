import { useCallback, useReducer, useRef } from 'react'
import * as DocumentService from '../services/DocumentService'
import * as EvidenceService from '../services/EvidenceService'
import { ApiError } from '../services/API'
import { useToast } from './useToast'
import { evidenceRunReducer, initialRunState } from './evidenceRunReducer'
import type { EvidenceScope } from '../services/EvidenceService'
import type { YearRange } from '../constants/yearRange'
import type { EvidenceCategory } from '../services/types/EvidenceTypes'

export type RunTarget =
  | { kind: 'documents-only' }
  | { kind: 'checklist' }
  | { kind: 'category'; categoryId: string }
  | { kind: 'question'; categoryId: string; questionId: string }

interface UseEvidenceRunOptions {
  tckr: string
  range: YearRange
  onResult: (categories: EvidenceCategory[]) => void
}

function scopeOf(target: RunTarget): EvidenceScope {
  if (target.kind === 'category') return { categoryId: target.categoryId }
  if (target.kind === 'question') return { categoryId: target.categoryId, questionId: target.questionId }
  return {}
}

export function useEvidenceRun({ tckr, range, onResult }: UseEvidenceRunOptions) {
  const [state, dispatch] = useReducer(evidenceRunReducer, initialRunState)
  const controllerRef = useRef<AbortController | null>(null)
  const activeRef = useRef(false)
  const { showToast } = useToast()

  const cancel = useCallback(() => {
    controllerRef.current?.abort()
    activeRef.current = false
    dispatch({ type: 'reset' })
  }, [])

  const start = useCallback(
    async (target: RunTarget) => {
      if (activeRef.current) return
      activeRef.current = true
      const controller = new AbortController()
      controllerRef.current = controller
      dispatch({ type: 'reset' })
      let failed = false

      const fail = (detail: string) => {
        failed = true
        dispatch({ type: 'error', detail })
        showToast({ kind: 'error', message: detail })
      }

      try {
        await DocumentService.streamDocuments(
          tckr,
          range,
          (frame) => {
            if (frame.type === 'start') dispatch({ type: 'docs-start', total: frame.total, counts: frame.counts })
            else if (frame.type === 'progress')
              dispatch({ type: 'docs-progress', completed: frame.completed, total: frame.total, form: frame.form })
            else if (frame.type === 'error') fail(frame.detail)
          },
          controller.signal,
        )

        if (failed) return
        if (target.kind === 'documents-only') {
          dispatch({ type: 'done' })
          return
        }

        dispatch({ type: 'begin-run' })
        await EvidenceService.streamEvidenceRun(
          tckr,
          range,
          scopeOf(target),
          (frame) => {
            if (frame.type === 'start') dispatch({ type: 'run-start', total: frame.total, cached: frame.cached })
            else if (frame.type === 'progress')
              dispatch({
                type: 'run-progress',
                completed: frame.completed,
                total: frame.total,
                current: { form: frame.form, year: frame.year, section: frame.section },
              })
            else if (frame.type === 'result') {
              onResult(frame.categories)
              dispatch({ type: 'done' })
            } else if (frame.type === 'error') fail(frame.detail)
          },
          controller.signal,
        )
      } catch (err) {
        fail(err instanceof ApiError ? err.detail : 'Checklist run failed')
      } finally {
        activeRef.current = false
      }
    },
    [tckr, range, onResult, showToast],
  )

  return { state, start, cancel }
}
