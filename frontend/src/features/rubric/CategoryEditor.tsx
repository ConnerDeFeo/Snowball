import { useEffect, useState } from 'react'
import { useOutletContext, useParams } from 'react-router-dom'
import Card from '../../shared/Card'
import Button from '../../shared/Button'
import TextArea from '../../shared/TextArea'
import TextInput from '../../shared/TextInput'
import Spinner from '../../shared/Spinner'
import SubAgentList from './SubAgentList'
import * as RubricService from '../../services/RubricService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'
import { displayCategory } from '../../constants/categories'
import type { RubricCategory } from '../../enums/RubricCategory'
import type { useRubric } from '../../hooks/useRubric'

function CategoryEditor() {
  const { category } = useParams<{ category: string }>()
  const rubric = useOutletContext<ReturnType<typeof useRubric>>()
  const { showToast } = useToast()
  const cat = category as RubricCategory
  const shape = rubric.shapes.get(cat)

  const [name, setName] = useState('')
  const [directions, setDirections] = useState(shape?.directions ?? '')
  const [busy, setBusy] = useState(false)
  const [confirmingDelete, setConfirmingDelete] = useState(false)

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- resets the local form when the selected category changes
    setDirections(shape?.directions ?? '')
    setName('')
    setConfirmingDelete(false)
  }, [cat, shape?.directions])

  async function handleCreate() {
    setBusy(true)
    try {
      await RubricService.createMeta(cat, { name, directions })
      showToast({ kind: 'info', message: `Created ${displayCategory(cat)} rubric` })
      await rubric.refresh()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to create rubric' })
    } finally {
      setBusy(false)
    }
  }

  async function handleSave() {
    setBusy(true)
    try {
      await RubricService.patchDirections(cat, { directions })
      showToast({ kind: 'info', message: 'Directions saved' })
      await rubric.refresh()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to save directions' })
    } finally {
      setBusy(false)
    }
  }

  async function handleDelete() {
    if (!confirmingDelete) {
      setConfirmingDelete(true)
      setTimeout(() => setConfirmingDelete(false), 3000)
      return
    }
    setBusy(true)
    try {
      await RubricService.deleteMeta(cat)
      showToast({ kind: 'info', message: `Deleted ${displayCategory(cat)} rubric` })
      await rubric.refresh()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to delete rubric' })
    } finally {
      setBusy(false)
      setConfirmingDelete(false)
    }
  }

  if (!shape) {
    return (
      <Card>
        <h2 className="text-xl font-bold text-slate-800">{displayCategory(cat)}</h2>
        <p className="mt-1 text-sm text-slate-500">This category has no rubric configured yet.</p>
        <div className="mt-4 flex flex-col gap-3">
          <TextInput value={name} onChange={setName} placeholder="Display name" />
          <TextArea value={directions} onChange={setDirections} placeholder="Grading directions..." rows={6} />
          <div>
            <Button onClick={handleCreate} disabled={busy || !name || !directions}>
              {busy ? <Spinner /> : 'Create rubric'}
            </Button>
          </div>
        </div>
      </Card>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-slate-800">{shape.name}</h2>
          <span className="text-xs text-slate-400">{shape.version}</span>
        </div>
        <TextArea value={directions} onChange={setDirections} rows={6} />
        <div className="mt-4 flex items-center gap-3">
          <Button onClick={handleSave} disabled={busy || directions === shape.directions}>
            {busy ? <Spinner /> : 'Save directions'}
          </Button>
          <Button variant="ghost" onClick={handleDelete} disabled={busy}>
            {confirmingDelete ? 'Confirm delete' : 'Delete rubric'}
          </Button>
        </div>
      </Card>
      <SubAgentList category={cat} shape={shape} onChanged={rubric.refresh} />
    </div>
  )
}

export default CategoryEditor
