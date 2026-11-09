import { useState } from 'react'
import Button from '../../shared/Button'
import QuestionEditor from './QuestionEditor'
import * as ChecklistService from '../../services/ChecklistService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'
import { displaySection } from '../../constants/categories'
import type { Question } from '../../services/types/ChecklistTypes'

interface QuestionItemProps {
  categoryId: string
  question: Question
  onChanged: () => void
}

function QuestionItem({ categoryId, question, onChanged }: QuestionItemProps) {
  const { showToast } = useToast()
  const [editing, setEditing] = useState(false)
  const [confirmingDelete, setConfirmingDelete] = useState(false)

  async function handleDelete() {
    if (!confirmingDelete) {
      setConfirmingDelete(true)
      setTimeout(() => setConfirmingDelete(false), 3000)
      return
    }
    try {
      await ChecklistService.deleteQuestion(categoryId, question.id)
      showToast({ kind: 'info', message: 'Question removed' })
      onChanged()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to delete question' })
    } finally {
      setConfirmingDelete(false)
    }
  }

  return (
    <li className="rounded-lg border border-secondary-ice p-3">
      {editing ? (
        <QuestionEditor
          categoryId={categoryId}
          existing={question}
          nextOrder={question.order}
          onDone={() => {
            setEditing(false)
            onChanged()
          }}
          onCancel={() => setEditing(false)}
        />
      ) : (
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-slate-800">{question.text}</p>
            <p className="mt-1 text-xs text-slate-400">
              {question.form} · {displaySection(question.section)}
              {question.latest_only && ' · Latest filing only'}
            </p>
          </div>
          <div className="flex shrink-0 gap-2">
            <Button variant="ghost" onClick={() => setEditing(true)}>
              Edit
            </Button>
            <Button variant="ghost" onClick={handleDelete}>
              {confirmingDelete ? 'Confirm' : 'Delete'}
            </Button>
          </div>
        </div>
      )}
    </li>
  )
}

export default QuestionItem
