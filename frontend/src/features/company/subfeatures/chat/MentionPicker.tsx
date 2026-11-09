import { useState } from 'react'
import Select from '../../../../shared/Select'
import Button from '../../../../shared/Button'
import { SECTION_FORMS } from '../../../../enums/FormType'
import { sectionsForForm } from '../../../../enums/Sections'
import { QUARTERS } from '../../../../constants/quarters'
import { displaySection } from '../../../../constants/categories'
import type { YearRange } from '../../../../constants/yearRange'
import type { SectionForm } from '../../../../enums/FormType'
import type { Mention } from '../../../../services/types/ReviewTypes'

interface MentionPickerProps {
  range: YearRange
  onAdd: (mention: Mention) => void
  onClose: () => void
}

function MentionPicker({ range, onAdd, onClose }: MentionPickerProps) {
  const [form, setForm] = useState<SectionForm>(SECTION_FORMS[0])
  const [year, setYear] = useState(String(range.end))
  const [quarter, setQuarter] = useState<string>(QUARTERS[0])
  const [section, setSection] = useState<string>(sectionsForForm(SECTION_FORMS[0])[0])

  const years = Array.from({ length: range.end - range.start + 1 }, (_, i) => String(range.end - i))

  function handleFormChange(next: string) {
    const typed = next as SectionForm
    setForm(typed)
    setSection(sectionsForForm(typed)[0])
  }

  function handleAdd() {
    onAdd({ form, year, ...(form === '10-Q' && { quarter }), section })
    onClose()
  }

  return (
    <div className="flex flex-col gap-2 rounded-lg border border-secondary-ice bg-secondary-ice/30 p-3">
      <div className="flex gap-2">
        <Select value={form} onChange={handleFormChange} options={SECTION_FORMS.map((f) => ({ value: f, label: f }))} />
        <Select value={year} onChange={setYear} options={years.map((y) => ({ value: y, label: y }))} />
        {form === '10-Q' && (
          <Select value={quarter} onChange={setQuarter} options={QUARTERS.map((q) => ({ value: q, label: q }))} />
        )}
      </div>
      <Select
        value={section}
        onChange={setSection}
        options={sectionsForForm(form).map((s) => ({ value: s, label: displaySection(s) }))}
      />
      <div className="flex gap-2">
        <Button onClick={handleAdd}>Add</Button>
        <Button variant="ghost" onClick={onClose}>
          Cancel
        </Button>
      </div>
    </div>
  )
}

export default MentionPicker
