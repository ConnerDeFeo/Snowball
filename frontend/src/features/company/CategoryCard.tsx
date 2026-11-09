import AnsweredBadge from '../../shared/AnsweredBadge'
import { countAnswered } from './evidenceStats'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface CategoryCardProps {
  category: EvidenceCategory
  selected: boolean
  onSelect: () => void
}

function CategoryCard({ category, selected, onSelect }: CategoryCardProps) {
  return (
    <button
      onClick={onSelect}
      className={`flex flex-col items-start gap-2 rounded-xl border p-4 text-left transition-colors ${
        selected ? 'border-secondary bg-secondary-ice/60' : 'border-secondary-ice bg-white/70 hover:bg-secondary-ice/40'
      }`}
    >
      <p className="text-sm font-medium text-slate-800">{category.name}</p>
      <AnsweredBadge answered={countAnswered(category)} total={category.questions.length} />
    </button>
  )
}

export default CategoryCard
