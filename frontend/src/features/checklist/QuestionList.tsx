import { useState } from 'react'
import Card from '../../shared/Card'
import Button from '../../shared/Button'
import QuestionEditor from './QuestionEditor'
import QuestionItem from './QuestionItem'
import type { Category } from '../../services/types/ChecklistTypes'

interface QuestionListProps {
  category: Category
  onChanged: () => void
}

function QuestionList({ category, onChanged }: QuestionListProps) {
  const [adding, setAdding] = useState(false)

  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-slate-800">Questions</h3>
        <Button variant="ghost" onClick={() => setAdding(true)} disabled={adding}>
          Add question
        </Button>
      </div>

      {adding && (
        <div className="mt-4 border-t border-secondary-ice pt-4">
          <QuestionEditor
            categoryId={category.id}
            existing={null}
            nextOrder={category.questions.length}
            onDone={() => {
              setAdding(false)
              onChanged()
            }}
            onCancel={() => setAdding(false)}
          />
        </div>
      )}

      <ul className="mt-4 flex flex-col gap-3">
        {category.questions.length === 0 && !adding && (
          <p className="text-sm text-slate-500">No questions in this category yet.</p>
        )}
        {category.questions.map((question) => (
          <QuestionItem key={question.id} categoryId={category.id} question={question} onChanged={onChanged} />
        ))}
      </ul>
    </Card>
  )
}

export default QuestionList
