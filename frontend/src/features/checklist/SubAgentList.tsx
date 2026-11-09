import { useState } from 'react'
import Button from '../../shared/Button'
import SubAgentEditor from './SubAgentEditor'
import * as ChecklistService from '../../services/ChecklistService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'
import { displaySection } from '../../constants/categories'
import type { Question, SubAgent } from '../../services/types/ChecklistTypes'

interface SubAgentListProps {
  categoryId: string
  question: Question
  onChanged: () => void
}

function SubAgentList({ categoryId, question, onChanged }: SubAgentListProps) {
  const { showToast } = useToast()
  const [adding, setAdding] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)

  async function handleDelete(subAgent: SubAgent) {
    try {
      await ChecklistService.deleteSubAgent(categoryId, question.id, subAgent.id)
      showToast({ kind: 'info', message: 'Sub-agent removed' })
      onChanged()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to delete sub-agent' })
    }
  }

  return (
    <div className="mt-3 border-t border-secondary-ice pt-3">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Sub-agents</p>
        <Button variant="ghost" onClick={() => setAdding(true)} disabled={adding}>
          Add sub-agent
        </Button>
      </div>

      {adding && (
        <div className="mt-3">
          <SubAgentEditor
            categoryId={categoryId}
            questionId={question.id}
            existing={null}
            onDone={() => {
              setAdding(false)
              onChanged()
            }}
            onCancel={() => setAdding(false)}
          />
        </div>
      )}

      <ul className="mt-3 flex flex-col gap-2">
        {question.sub_agents.length === 0 && !adding && (
          <p className="text-sm text-slate-500">No sub-agents yet, so this question can't produce evidence.</p>
        )}
        {question.sub_agents.map((subAgent) => (
          <li key={subAgent.id} className="rounded-lg bg-secondary-ice/30 p-3">
            {editingId === subAgent.id ? (
              <SubAgentEditor
                categoryId={categoryId}
                questionId={question.id}
                existing={subAgent}
                onDone={() => {
                  setEditingId(null)
                  onChanged()
                }}
                onCancel={() => setEditingId(null)}
              />
            ) : (
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-medium text-slate-800">
                    {subAgent.form} · {displaySection(subAgent.section)}
                  </p>
                  <p className="mt-1 line-clamp-2 text-xs text-slate-500">{subAgent.prompt}</p>
                </div>
                <div className="flex shrink-0 gap-2">
                  <Button variant="ghost" onClick={() => setEditingId(subAgent.id)}>
                    Edit
                  </Button>
                  <Button variant="ghost" onClick={() => handleDelete(subAgent)}>
                    Delete
                  </Button>
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default SubAgentList
