import CategoryDetail from './CategoryDetail'
import RunBanner from './RunBanner'
import EmptyState from '../../shared/EmptyState'
import type { RunTarget } from '../../hooks/useEvidenceRun'
import type { RunState } from '../../hooks/evidenceRunReducer'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface ChecklistViewProps {
  categories: EvidenceCategory[]
  selectedId: string | undefined
  loading: boolean
  error: string | null
  onRetry: () => void
  active: boolean
  state: RunState
  onStart: (target: RunTarget) => void
  onEdit: () => void
}

function ChecklistView({ categories, selectedId, loading, error, onRetry, active, state, onStart, onEdit }: ChecklistViewProps) {
  const selected = categories.find((c) => c.id === selectedId) ?? categories[0]

  if (loading && !selected) return <div className="h-64 animate-pulse rounded-2xl bg-secondary-ice" />

  if (error && !selected) {
    return (
      <EmptyState
        title="Couldn't load evidence"
        description={error}
        action={<button onClick={onRetry} className="text-sm font-semibold text-secondary-deep underline">Retry</button>}
      />
    )
  }

  if (!selected) {
    return (
      <EmptyState
        title="No checklist yet"
        description="Add categories and questions to the checklist, then run it."
        action={<button onClick={onEdit} className="cursor-pointer text-sm font-semibold text-secondary-deep underline">Edit checklist</button>}
      />
    )
  }

  return (
    <div className="flex h-full flex-col gap-4">
      <RunBanner state={state} />
      <CategoryDetail
        category={selected}
        disabled={active}
        onRunCategory={() => onStart({ kind: 'category', categoryId: selected.id })}
        onRunQuestion={(questionId) => onStart({ kind: 'question', categoryId: selected.id, questionId })}
      />
    </div>
  )
}

export default ChecklistView
