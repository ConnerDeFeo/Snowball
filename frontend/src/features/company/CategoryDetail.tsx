import Button from '../../shared/Button'
import QuestionRow from './QuestionRow'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface CategoryDetailProps {
  category: EvidenceCategory
  disabled: boolean
  onRunCategory: () => void
  onRunQuestion: (questionId: string) => void
}

function CategoryDetail({ category, disabled, onRunCategory, onRunQuestion }: CategoryDetailProps) {
  return (
    <section className="min-w-0 flex-1 overflow-y-auto pr-1">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h3 className="text-lg font-bold text-slate-800">{category.name}</h3>
        <Button variant="subtle" size="sm" onClick={onRunCategory} disabled={disabled}>
          ↻ Run category
        </Button>
      </div>

      {category.questions.length === 0 ? (
        <p className="text-sm text-slate-500">This category has no questions yet.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {category.questions.map((q) => (
            <QuestionRow key={q.id} question={q} disabled={disabled} onRun={() => onRunQuestion(q.id)} />
          ))}
        </ul>
      )}
    </section>
  )
}

export default CategoryDetail
