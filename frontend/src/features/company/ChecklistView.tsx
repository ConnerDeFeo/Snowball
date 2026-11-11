import { useState } from 'react'
import { Link } from 'react-router-dom'
import CategorySidebar from './CategorySidebar'
import CategoryDetail from './CategoryDetail'
import EmptyState from '../../shared/EmptyState'
import type { RunTarget } from '../../hooks/useEvidenceRun'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface ChecklistViewProps {
  categories: EvidenceCategory[]
  loading: boolean
  error: string | null
  onRetry: () => void
  active: boolean
  onStart: (target: RunTarget) => void
}

function ChecklistView({ categories, loading, error, onRetry, active, onStart }: ChecklistViewProps) {
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
        action={<Link to="/checklist" className="text-sm font-semibold text-secondary-deep underline">Edit checklist</Link>}
      />
    )
  }

  return (
    <div className="flex h-full gap-6">
      <CategorySidebar categories={categories} selectedId={selected.id} onSelect={setSelectedId} />
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
