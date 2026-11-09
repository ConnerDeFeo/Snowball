import CategoryCard from './CategoryCard'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface CategoryGridProps {
  categories: EvidenceCategory[]
  selectedId: string | null
  onSelect: (categoryId: string) => void
}

function CategoryGrid({ categories, selectedId, onSelect }: CategoryGridProps) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
      {categories.map((category) => (
        <CategoryCard
          key={category.id}
          category={category}
          selected={selectedId === category.id}
          onSelect={() => onSelect(category.id)}
        />
      ))}
    </div>
  )
}

export default CategoryGrid
