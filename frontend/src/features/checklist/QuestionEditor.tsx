import { useState } from 'react'
import TextArea from '../../shared/TextArea'
import Checkbox from '../../shared/Checkbox'
import Button from '../../shared/Button'
import Spinner from '../../shared/Spinner'
import * as ChecklistService from '../../services/ChecklistService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'
import type { Question } from '../../services/types/ChecklistTypes'

interface QuestionEditorProps {
  categoryId: string
  existing: Question | null
  nextOrder: number
  onDone: () => void
  onCancel: () => void
}

function QuestionEditor({ categoryId, existing, nextOrder, onDone, onCancel }: QuestionEditorProps) {
  const { showToast } = useToast()
  const [text, setText] = useState(existing?.text ?? '')
  const [latestOnly, setLatestOnly] = useState(existing?.latest_only ?? false)
  const [busy, setBusy] = useState(false)

  async function handleSubmit() {
    setBusy(true)
    try {
      if (existing) {
        await ChecklistService.patchQuestion(categoryId, existing.id, { text: text.trim(), latest_only: latestOnly })
      } else {
        await ChecklistService.createQuestion(categoryId, { text: text.trim(), order: nextOrder, latest_only: latestOnly })
      }
      showToast({ kind: 'info', message: 'Question saved' })
      onDone()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to save question' })
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="flex flex-col gap-3">
      <TextArea value={text} onChange={setText} placeholder="Question to answer from the filings..." rows={3} />
      <Checkbox checked={latestOnly} onChange={setLatestOnly} label="Only look at the latest filing in the range" />
      <div className="flex gap-3">
        <Button onClick={handleSubmit} disabled={busy || !text.trim()}>
          {busy ? <Spinner /> : 'Save'}
        </Button>
        <Button variant="ghost" onClick={onCancel} disabled={busy}>
          Cancel
        </Button>
      </div>
    </div>
  )
}

export default QuestionEditor
