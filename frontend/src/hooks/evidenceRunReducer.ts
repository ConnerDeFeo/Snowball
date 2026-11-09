export interface RunCurrent {
  form: string
  year: string
  section: string
}

export type RunState =
  | { phase: 'idle' }
  | { phase: 'fetching-docs'; completed: number; total: number; counts?: Record<string, number>; currentForm?: string }
  | { phase: 'running'; completed: number; total: number; cached?: number; current?: RunCurrent }
  | { phase: 'done' }
  | { phase: 'error'; detail: string }

export type RunAction =
  | { type: 'reset' }
  | { type: 'docs-start'; total: number; counts: Record<string, number> }
  | { type: 'docs-progress'; completed: number; total: number; form: string }
  | { type: 'begin-run' }
  | { type: 'run-start'; total: number; cached: number }
  | { type: 'run-progress'; completed: number; total: number; current: RunCurrent }
  | { type: 'done' }
  | { type: 'error'; detail: string }

export function evidenceRunReducer(state: RunState, action: RunAction): RunState {
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
    case 'begin-run':
      return { phase: 'running', completed: 0, total: 0 }
    case 'run-start':
      return { phase: 'running', completed: 0, total: action.total, cached: action.cached }
    case 'run-progress':
      return {
        phase: 'running',
        completed: action.completed,
        total: action.total,
        cached: state.phase === 'running' ? state.cached : undefined,
        current: action.current,
      }
    // A fully cached run can finish with no start/progress frames at all, so
    // 'done' must be reachable from any state.
    case 'done':
      return { phase: 'done' }
    case 'error':
      return { phase: 'error', detail: action.detail }
    default:
      return state
  }
}

export const initialRunState: RunState = { phase: 'idle' }
