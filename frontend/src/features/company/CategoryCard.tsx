import GradeBadge from '../../shared/GradeBadge'
import { displayCategory } from '../../constants/categories'
import type { RubricCategory } from '../../enums/RubricCategory'
import type { GradedTimePeriod } from '../../services/types/GradingTypes'

interface CategoryCardProps {
  category: RubricCategory
  graded?: GradedTimePeriod
  selected: boolean
  onSelect: () => void
}

function CategoryCard({ category, graded, selected, onSelect }: CategoryCardProps) {
  return (
    <button
      onClick={onSelect}
      className={`flex flex-col items-start gap-2 rounded-xl border p-4 text-left transition-colors ${
        selected ? 'border-secondary bg-secondary-ice/60' : 'border-secondary-ice bg-white/70 hover:bg-secondary-ice/40'
      }`}
    >
      <p className="text-sm font-medium text-slate-800">{displayCategory(category)}</p>
      <GradeBadge graded={graded} />
    </button>
  )
}

export default CategoryCard
