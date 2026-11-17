import { useState } from 'react'
import CategorySidebar from './CategorySidebar'
import CategoryDetail from './CategoryDetail'
import CompanyActions from './CompanyActions'
import RunBanner from './RunBanner'
import EmptyState from '../../shared/EmptyState'
import type { RunTarget } from '../../hooks/useEvidenceRun'
import type { RunState } from '../../hooks/evidenceRunReducer'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface ChecklistViewProps {
  categories: EvidenceCategory[]
  loading: boolean
  error: string | null
  onRetry: () => void
  active: boolean
  state: RunState
  onStart: (target: RunTarget) => void
  onRun: () => void
  onCancel: () => void
  onEdit: () => void
}

function ChecklistView({ categories, loading, error, onRetry, active, state, onStart, onRun, onCancel, onEdit }: ChecklistViewProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
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
    <div className="flex h-full gap-6">
      <div className="flex w-56 shrink-0 flex-col gap-3 overflow-y-auto">
        <CategorySidebar categories={categories} selectedId={selected.id} onSelect={setSelectedId} />
        <CompanyActions active={active} onRun={onRun} onCancel={onCancel} />
        <RunBanner state={state} />
      </div>
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
