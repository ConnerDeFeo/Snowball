import { useState } from 'react'
import Select from '../../shared/Select'
import TextArea from '../../shared/TextArea'
import Button from '../../shared/Button'
import Spinner from '../../shared/Spinner'
import * as ChecklistService from '../../services/ChecklistService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'
import { SUB_AGENT_FORMS } from '../../enums/FormType'
import { sectionsForForm } from '../../enums/Sections'
import { displaySection } from '../../constants/categories'
import type { SubAgentForm } from '../../enums/FormType'
import type { Section } from '../../enums/Sections'
import type { SubAgent } from '../../services/types/ChecklistTypes'

interface SubAgentEditorProps {
  categoryId: string
  questionId: string
  existing: SubAgent | null
  onDone: () => void
  onCancel: () => void
}

function SubAgentEditor({ categoryId, questionId, existing, onDone, onCancel }: SubAgentEditorProps) {
  const { showToast } = useToast()
  const [form, setForm] = useState<SubAgentForm>(existing?.form ?? SUB_AGENT_FORMS[0])
  const [section, setSection] = useState<Section>(existing?.section ?? sectionsForForm(SUB_AGENT_FORMS[0])[0])
  const [prompt, setPrompt] = useState(existing?.prompt ?? '')
  const [busy, setBusy] = useState(false)

  function handleFormChange(nextForm: string) {
    const typedForm = nextForm as SubAgentForm
    setForm(typedForm)
    setSection(sectionsForForm(typedForm)[0])
  }

  async function handleSubmit() {
    setBusy(true)
    try {
      const body = { form, section, prompt }
      if (existing) {
        await ChecklistService.patchSubAgent(categoryId, questionId, existing.id, body)
      } else {
        await ChecklistService.createSubAgent(categoryId, questionId, body)
      }
      showToast({ kind: 'info', message: 'Sub-agent saved' })
      onDone()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to save sub-agent' })
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex gap-3">
        <Select value={form} onChange={handleFormChange} options={SUB_AGENT_FORMS.map((f) => ({ value: f, label: f }))} />
        <Select
          value={section}
          onChange={(v) => setSection(v as Section)}
          options={sectionsForForm(form).map((s) => ({ value: s, label: displaySection(s) }))}
        />
      </div>
      <TextArea value={prompt} onChange={setPrompt} placeholder="What should this sub-agent look for in that section?" rows={4} />
      <div className="flex gap-3">
        <Button onClick={handleSubmit} disabled={busy || !prompt}>
          {busy ? <Spinner /> : 'Save'}
        </Button>
        <Button variant="ghost" onClick={onCancel} disabled={busy}>
          Cancel
        </Button>
      </div>
    </div>
  )
}

export default SubAgentEditor
