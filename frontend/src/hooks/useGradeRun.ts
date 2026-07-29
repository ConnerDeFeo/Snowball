import { useCallback, useReducer, useRef } from 'react'
import * as GradingService from '../services/GradingService'
import { ApiError } from '../services/API'
import { useToast } from './useToast'
import { gradeRunReducer, initialGradeRunState } from './gradeRunReducer'
import type { RubricCategory } from '../enums/RubricCategory'
import type { YearRange } from '../constants/yearRange'
import type { GradedTimePeriod } from '../services/types/GradingTypes'

export type GradeRunTarget =
  | { kind: 'documents-only' }
  | { kind: 'all' }
  | { kind: 'section'; category: RubricCategory }

interface UseGradeRunOptions {
  tckr: string
  range: YearRange
  onResult: (graded: GradedTimePeriod[]) => void
}

export function useGradeRun({ tckr, range, onResult }: UseGradeRunOptions) {
  const [state, dispatch] = useReducer(gradeRunReducer, initialGradeRunState)
  const controllerRef = useRef<AbortController | null>(null)
  const activeRef = useRef(false)
  const { showToast } = useToast()

  const cancel = useCallback(() => {
    controllerRef.current?.abort()
    activeRef.current = false
    dispatch({ type: 'reset' })
  }, [])

  const start = useCallback(
    async (target: GradeRunTarget) => {
      if (activeRef.current) return
      activeRef.current = true
      const controller = new AbortController()
      controllerRef.current = controller
      dispatch({ type: 'reset' })
      let failed = false

      try {
        await GradingService.streamDocuments(
          tckr,
          range,
          (frame) => {
            if (frame.type === 'start') dispatch({ type: 'docs-start', total: frame.total, counts: frame.counts })
            else if (frame.type === 'progress')
              dispatch({ type: 'docs-progress', completed: frame.completed, total: frame.total, form: frame.form })
            else if (frame.type === 'error') {
              failed = true
              dispatch({ type: 'error', detail: frame.detail })
              showToast({ kind: 'error', message: frame.detail })
            }
          },
          controller.signal,
        )

        if (failed) return
        if (target.kind === 'documents-only') {
          dispatch({ type: 'done' })
          return
        }

        dispatch({ type: 'begin-grading' })

        if (target.kind === 'all') {
          await GradingService.streamGradeAll(
            tckr,
            range,
            (frame) => {
              if (frame.type === 'categories') dispatch({ type: 'grade-categories', total: frame.total, cached: frame.cached })
              else if (frame.type === 'progress')
                dispatch({
                  type: 'grade-progress',
                  completed: frame.completed,
                  total: frame.total,
                  current: { category: frame.category, section: frame.section, form: frame.form, year: frame.year },
                })
              else if (frame.type === 'result') {
                onResult(frame.graded)
                dispatch({ type: 'done' })
              } else if (frame.type === 'error') {
                failed = true
                dispatch({ type: 'error', detail: frame.detail })
                showToast({ kind: 'error', message: frame.detail })
              }
            },
            controller.signal,
          )
        } else {
          await GradingService.streamGradeSection(
            tckr,
            range,
            target.category,
            (frame) => {
              if (frame.type === 'start') dispatch({ type: 'grade-start', total: frame.total })
              else if (frame.type === 'progress')
                dispatch({
                  type: 'grade-progress',
                  completed: frame.completed,
                  total: frame.total,
                  current: { section: frame.section, form: frame.form, year: frame.year },
                })
              else if (frame.type === 'result') {
                onResult([frame.graded])
                dispatch({ type: 'done' })
              } else if (frame.type === 'error') {
                failed = true
                dispatch({ type: 'error', detail: frame.detail })
                showToast({ kind: 'error', message: frame.detail })
              }
            },
            controller.signal,
          )
        }
      } catch (err) {
        const detail = err instanceof ApiError ? err.detail : 'Grading run failed'
        dispatch({ type: 'error', detail })
        showToast({ kind: 'error', message: detail })
      } finally {
        activeRef.current = false
      }
    },
    [tckr, range, onResult, showToast],
  )

  return { state, start, cancel }
}
