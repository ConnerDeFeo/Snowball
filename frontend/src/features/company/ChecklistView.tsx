import { Link } from 'react-router-dom'
import CategoryGrid from './CategoryGrid'
import CategoryDetail from './CategoryDetail'
import EmptyState from '../../shared/EmptyState'
import type { RunTarget } from '../../hooks/useEvidenceRun'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface ChecklistViewProps {
  categories: EvidenceCategory[]
  loading: boolean
  error: string | null
  onRetry: () => void
  selectedId: string | null
  onSelect: (id: string) => void
  active: boolean
  onStart: (target: RunTarget) => void
}

function ChecklistView({ categories, loading, error, onRetry, selectedId, onSelect, active, onStart }: ChecklistViewProps) {
  const selected = categories.find((c) => c.id === selectedId)
  const hasAny = categories.length > 0

  return (
    <>
      {loading && !hasAny ? (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-24 animate-pulse rounded-2xl bg-secondary-ice" />
          ))}
        </div>
      ) : error && !hasAny ? (
        <EmptyState
          title="Couldn't load evidence"
          description={error}
          action={
            <button onClick={onRetry} className="text-sm font-semibold text-secondary-deep underline">
              Retry
            </button>
          }
        />
      ) : !hasAny ? (
        <EmptyState
          title="No checklist yet"
          description="Add categories and questions to the checklist, then run it."
          action={
            <Link to="/checklist" className="text-sm font-semibold text-secondary-deep underline">
              Edit checklist
            </Link>
          }
        />
      ) : (
        <CategoryGrid categories={categories} selectedId={selectedId} onSelect={onSelect} />
      )}

      {selected && (
        <CategoryDetail
          category={selected}
          disabled={active}
          onRunCategory={() => onStart({ kind: 'category', categoryId: selected.id })}
          onRunQuestion={(questionId) => onStart({ kind: 'question', categoryId: selected.id, questionId })}
        />
      )}
    </>
  )
}

export default ChecklistView
