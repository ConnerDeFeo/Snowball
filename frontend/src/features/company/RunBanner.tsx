import Card from '../../shared/Card'
import ProgressBar from '../../shared/ProgressBar'
import Spinner from '../../shared/Spinner'
import Button from '../../shared/Button'
import { displaySection } from '../../constants/categories'
import type { RunState } from '../../hooks/evidenceRunReducer'
import type { Section } from '../../enums/Sections'

interface RunBannerProps {
  state: RunState
  onCancel: () => void
}

function RunBanner({ state, onCancel }: RunBannerProps) {
  if (state.phase === 'idle' || state.phase === 'done') return null

  if (state.phase === 'error') {
    return (
      <Card className="border-rose-200 bg-rose-50/70">
        <p className="text-sm font-medium text-rose-700">{state.detail}</p>
      </Card>
    )
  }

  const isDocs = state.phase === 'fetching-docs'
  const hasProgress = state.total > 0

  const label = isDocs
    ? `${state.completed}/${state.total}${state.currentForm ? ` · ${state.currentForm}` : ''}`
    : `${state.completed}/${state.total}${
        state.current
          ? ` · ${state.current.form} ${state.current.year} ${displaySection(state.current.section as Section)}`
          : ''
      }`

  return (
    <Card>
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-800">{isDocs ? 'Fetching filings' : 'Running checklist'}</p>
        <Button variant="ghost" onClick={onCancel}>
          Cancel
        </Button>
      </div>

      {!hasProgress && (
        <div className="mt-3 flex items-center gap-2 text-sm text-slate-500">
          <Spinner /> Starting…
        </div>
      )}

      {hasProgress && (
        <div className="mt-3">
          <ProgressBar completed={state.completed} total={state.total} label={label} />
        </div>
      )}

      {isDocs && state.counts && (
        <p className="mt-2 text-xs text-slate-400">
          {Object.entries(state.counts)
            .map(([form, count]) => `${count} ${form}`)
            .join(' · ')}
        </p>
      )}

      {!isDocs && state.cached !== undefined && state.cached > 0 && (
        <p className="mt-2 text-xs text-slate-400">{state.cached} already cached</p>
      )}
    </Card>
  )
}

export default RunBanner
