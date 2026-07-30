import Card from '../../shared/Card'
import Button from '../../shared/Button'
import GradeBadge from '../../shared/GradeBadge'
import { displayCategory } from '../../constants/categories'
import type { RubricCategory } from '../../enums/RubricCategory'
import type { GradedTimePeriod } from '../../services/types/GradingTypes'

interface CategoryDetailProps {
  category: RubricCategory
  graded?: GradedTimePeriod
  onGradeThis: () => void
  disabled: boolean
}

function CategoryDetail({ category, graded, onGradeThis, disabled }: CategoryDetailProps) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-slate-800">{displayCategory(category)}</h3>
        <GradeBadge graded={graded} />
      </div>

      {graded ? (
        <>
          <p className="mt-3 text-sm text-slate-600">{graded.reasoning}</p>
          {graded.quotes.length > 0 && (
            <div className="mt-3 flex flex-col gap-2">
              {graded.quotes.map((quote, i) => (
                <blockquote key={i} className="border-l-2 border-secondary pl-3 text-sm italic text-slate-500">
                  {quote}
                </blockquote>
              ))}
            </div>
          )}
        </>
      ) : (
        <p className="mt-3 text-sm text-slate-500">This category hasn't been graded yet.</p>
      )}
      {!graded && 
        <div className="mt-4">
          <Button variant="ghost" onClick={onGradeThis} disabled={disabled}>
            Grade this category
          </Button>
        </div>
      }
    </Card>
  )
}

export default CategoryDetail
