export interface GradingCurrent {
  category?: string
  section: string
  form: string
  year: number
}

export type GradeRunState =
  | { phase: 'idle' }
  | { phase: 'fetching-docs'; completed: number; total: number; counts?: Record<string, number>; currentForm?: string }
  | { phase: 'grading'; completed: number; total: number; cached?: number; current?: GradingCurrent }
  | { phase: 'done' }
  | { phase: 'error'; detail: string }

export type GradeRunAction =
  | { type: 'reset' }
  | { type: 'docs-start'; total: number; counts: Record<string, number> }
  | { type: 'docs-progress'; completed: number; total: number; form: string }
  | { type: 'begin-grading' }
  | { type: 'grade-categories'; total: number; cached: number }
  | { type: 'grade-start'; total: number }
  | { type: 'grade-progress'; completed: number; total: number; current: GradingCurrent }
  | { type: 'done' }
  | { type: 'error'; detail: string }

export function gradeRunReducer(state: GradeRunState, action: GradeRunAction): GradeRunState {
  switch (action.type) {
    case 'reset':
      return { phase: 'idle' }
    case 'docs-start':
      return { phase: 'fetching-docs', completed: 0, total: action.total, counts: action.counts }
    case 'docs-progress':
      return {
        phase: 'fetching-docs',
        completed: action.completed,
        total: action.total,
        counts: state.phase === 'fetching-docs' ? state.counts : undefined,
        currentForm: action.form,
      }
    case 'begin-grading':
      return { phase: 'grading', completed: 0, total: 0 }
    case 'grade-categories':
      return { phase: 'grading', completed: 0, total: 0, cached: action.cached }
    case 'grade-start':
      return { phase: 'grading', completed: 0, total: action.total }
    case 'grade-progress':
      return {
        phase: 'grading',
        completed: action.completed,
        total: action.total,
        current: action.current,
      }
    // A cache hit / no-evidence result can arrive with no preceding start/progress
    // frames at all, so 'done' must be reachable from any state.
    case 'done':
      return { phase: 'done' }
    case 'error':
      return { phase: 'error', detail: action.detail }
    default:
      return state
  }
}

export const initialGradeRunState: GradeRunState = { phase: 'idle' }
