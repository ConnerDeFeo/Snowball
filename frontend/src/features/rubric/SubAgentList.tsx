import { useState } from 'react'
import Card from '../../shared/Card'
import Button from '../../shared/Button'
import SubAgentEditor from './SubAgentEditor'
import * as RubricService from '../../services/RubricService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'
import { displaySection } from '../../constants/categories'
import type { RubricCategory } from '../../enums/RubricCategory'
import type { RubricShape } from '../../services/types/RubricTypes'
import type { SubAgentForm } from '../../enums/FormType'
import type { Section } from '../../enums/Sections'

interface SubAgentListProps {
  category: RubricCategory
  shape: RubricShape
  onChanged: () => void
}

interface ParsedEntry {
  key: string
  form: SubAgentForm
  section: Section
  prompt: string
}

function parseEntries(shape: RubricShape): ParsedEntry[] {
  return Object.entries(shape.sub_agent_directions).map(([key, direction]) => {
    const [form, section] = key.split('#')
    return { key, form: form as SubAgentForm, section: section as Section, prompt: direction.prompt }
  })
}

function SubAgentList({ category, shape, onChanged }: SubAgentListProps) {
  const { showToast } = useToast()
  const [adding, setAdding] = useState(false)
  const [editingKey, setEditingKey] = useState<string | null>(null)

  const entries = parseEntries(shape)

  async function handleDelete(entry: ParsedEntry) {
    try {
      await RubricService.deleteSubAgent(category, entry.form, entry.section)
      showToast({ kind: 'info', message: 'Sub-agent removed' })
      onChanged()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to delete sub-agent' })
    }
  }

  return (
    <Card>
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-slate-800">Sub-agents</h3>
        <Button variant="ghost" onClick={() => setAdding(true)} disabled={adding}>
          Add sub-agent
        </Button>
      </div>

      {adding && (
        <div className="mt-4 border-t border-secondary-ice pt-4">
          <SubAgentEditor
            category={category}
            existing={null}
            onDone={() => {
              setAdding(false)
              onChanged()
            }}
            onCancel={() => setAdding(false)}
          />
        </div>
      )}

      <ul className="mt-4 flex flex-col gap-2">
        {entries.length === 0 && !adding && (
          <p className="text-sm text-slate-500">No sub-agents configured for this category.</p>
        )}
        {entries.map((entry) => (
          <li key={entry.key} className="rounded-lg border border-secondary-ice p-3">
            {editingKey === entry.key ? (
              <SubAgentEditor
                category={category}
                existing={entry}
                onDone={() => {
                  setEditingKey(null)
                  onChanged()
                }}
                onCancel={() => setEditingKey(null)}
              />
            ) : (
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-medium text-slate-800">
                    {entry.form} · {displaySection(entry.section)}
                  </p>
                  <p className="mt-1 line-clamp-2 text-xs text-slate-500">{entry.prompt}</p>
                </div>
                <div className="flex shrink-0 gap-2">
                  <Button variant="ghost" onClick={() => setEditingKey(entry.key)}>
                    Edit
                  </Button>
                  <Button variant="ghost" onClick={() => handleDelete(entry)}>
                    Delete
                  </Button>
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>
    </Card>
  )
}

export default SubAgentList
