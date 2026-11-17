import AnsweredBadge from '../../shared/AnsweredBadge'
import { countAnswered } from '../company/evidenceStats'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface CategoryNavProps {
  categories: EvidenceCategory[]
  selectedId: string | undefined
  onSelect: (id: string) => void
}

function CategoryNav({ categories, selectedId, onSelect }: CategoryNavProps) {
  return (
    <div className="ml-3 flex flex-col gap-1 border-l border-secondary-ice pl-2">
      {categories.map((c) => (
        <button
          key={c.id}
          data-close
          onClick={() => onSelect(c.id)}
          className={`flex cursor-pointer items-center justify-between gap-2 rounded-lg px-3 py-1.5 text-left text-sm transition-colors ${
            c.id === selectedId ? 'bg-white font-semibold text-secondary-deep shadow-sm' : 'text-slate-600 hover:bg-white/60'
          }`}
        >
          <span className="truncate">{c.name}</span>
          <AnsweredBadge answered={countAnswered(c)} total={c.questions.length} />
        </button>
      ))}
    </div>
  )
}

export default CategoryNav
