import ProgressBar from '../../shared/ProgressBar'
import { displaySection } from '../../constants/categories'
import type { RunState } from '../../hooks/evidenceRunReducer'
import type { Section } from '../../enums/Sections'

interface RunBannerProps {
  state: RunState
}

// Compact progress for the sidebar: a bar with a short title, and the current filing below it.
function RunBanner({ state }: RunBannerProps) {
  if (state.phase === 'idle' || state.phase === 'done') return null

  if (state.phase === 'error') {
    return <p className="text-sm font-medium text-rose-700">{state.detail}</p>
  }

  const isDocs = state.phase === 'fetching-docs'
  const where = isDocs
    ? state.currentForm
    : state.current && `${state.current.form} ${state.current.year} ${displaySection(state.current.section as Section)}`
  const title = isDocs ? 'Filings' : 'Checklist'
  const label = state.total > 0 ? `${title} ${state.completed}/${state.total}` : `${title}…`

  return (
    <div>
      <ProgressBar completed={state.completed} total={state.total} label={label} />
      {where && <p className="mt-1 truncate text-xs text-slate-400">{where}</p>}
    </div>
  )
}

export default RunBanner
