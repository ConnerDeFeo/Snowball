import Card from '../../shared/Card'
import Button from '../../shared/Button'
import AnsweredBadge from '../../shared/AnsweredBadge'
import QuestionRow from './QuestionRow'
import { countAnswered } from './evidenceStats'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface CategoryDetailProps {
  category: EvidenceCategory
  disabled: boolean
  onRunCategory: () => void
  onRunQuestion: (questionId: string) => void
}

function CategoryDetail({ category, disabled, onRunCategory, onRunQuestion }: CategoryDetailProps) {
  return (
    <Card>
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <h3 className="text-lg font-bold text-slate-800">{category.name}</h3>
          <AnsweredBadge answered={countAnswered(category)} total={category.questions.length} />
        </div>
        <Button variant="ghost" onClick={onRunCategory} disabled={disabled}>
          Run category
        </Button>
      </div>

      {category.questions.length === 0 ? (
        <p className="mt-3 text-sm text-slate-500">This category has no questions yet.</p>
      ) : (
        <ul className="mt-4 flex flex-col gap-2">
          {category.questions.map((question) => (
            <QuestionRow
              key={question.id}
              question={question}
              disabled={disabled}
              onRun={() => onRunQuestion(question.id)}
            />
          ))}
        </ul>
      )}
    </Card>
  )
}

export default CategoryDetail
