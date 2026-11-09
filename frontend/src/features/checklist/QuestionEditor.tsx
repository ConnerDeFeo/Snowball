import { useState } from 'react'
import Select from '../../shared/Select'
import TextArea from '../../shared/TextArea'
import Checkbox from '../../shared/Checkbox'
import Button from '../../shared/Button'
import Spinner from '../../shared/Spinner'
import * as ChecklistService from '../../services/ChecklistService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'
import { SECTION_FORMS } from '../../enums/FormType'
import { sectionsForForm } from '../../enums/Sections'
import { displaySection } from '../../constants/categories'
import type { SectionForm } from '../../enums/FormType'
import type { Section } from '../../enums/Sections'
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
  const [form, setForm] = useState<SectionForm>(existing?.form ?? SECTION_FORMS[0])
  const [section, setSection] = useState<Section>(existing?.section ?? sectionsForForm(SECTION_FORMS[0])[0])
  const [latestOnly, setLatestOnly] = useState(existing?.latest_only ?? false)
  const [busy, setBusy] = useState(false)

  function handleFormChange(nextForm: string) {
    const typedForm = nextForm as SectionForm
    setForm(typedForm)
    setSection(sectionsForForm(typedForm)[0])
  }

  async function handleSubmit() {
    setBusy(true)
    try {
      if (existing) {
        await ChecklistService.patchQuestion(categoryId, existing.id, { text: text.trim(), form, section, latest_only: latestOnly })
      } else {
        await ChecklistService.createQuestion(categoryId, { text: text.trim(), form, section, order: nextOrder, latest_only: latestOnly })
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
      <div className="flex gap-3">
        <Select value={form} onChange={handleFormChange} options={SECTION_FORMS.map((f) => ({ value: f, label: f }))} />
        <Select
          value={section}
          onChange={(v) => setSection(v as Section)}
          options={sectionsForForm(form).map((s) => ({ value: s, label: displaySection(s) }))}
        />
      </div>
      <TextArea value={text} onChange={setText} placeholder="What should the agent look for in that section?" rows={3} />
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
