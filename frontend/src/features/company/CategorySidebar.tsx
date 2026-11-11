import AnsweredBadge from '../../shared/AnsweredBadge'
import { countAnswered } from './evidenceStats'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface CategorySidebarProps {
  categories: EvidenceCategory[]
  selectedId: string
  onSelect: (id: string) => void
}

function CategorySidebar({ categories, selectedId, onSelect }: CategorySidebarProps) {
  return (
    <nav className="flex w-56 shrink-0 flex-col gap-1 overflow-y-auto">
      {categories.map((c) => (
        <button
          key={c.id}
          onClick={() => onSelect(c.id)}
          className={`flex cursor-pointer items-center justify-between gap-2 rounded-lg px-3 py-2 text-left text-sm transition-colors ${
            c.id === selectedId ? 'bg-secondary-ice font-semibold text-secondary-deep' : 'text-slate-600 hover:bg-secondary-ice/50'
          }`}
        >
          <span className="truncate">{c.name}</span>
          <AnsweredBadge answered={countAnswered(c)} total={c.questions.length} />
        </button>
      ))}
    </nav>
  )
}

export default CategorySidebar
