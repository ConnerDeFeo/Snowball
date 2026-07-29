import CategoryCard from './CategoryCard'
import { RUBRIC_CATEGORIES } from '../../enums/RubricCategory'
import type { RubricCategory } from '../../enums/RubricCategory'
import type { GradedTimePeriod } from '../../services/types/GradingTypes'

interface GradesGridProps {
  grades: Map<string, GradedTimePeriod>
  selected: RubricCategory | null
  onSelect: (category: RubricCategory) => void
}

function GradesGrid({ grades, selected, onSelect }: GradesGridProps) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
      {RUBRIC_CATEGORIES.map((category) => (
        <CategoryCard
          key={category}
          category={category}
          graded={grades.get(category)}
          selected={selected === category}
          onSelect={() => onSelect(category)}
        />
      ))}
    </div>
  )
}

export default GradesGrid
