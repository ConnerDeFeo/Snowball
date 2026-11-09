import { useEffect, useState } from 'react'
import { useNavigate, useOutletContext, useParams } from 'react-router-dom'
import Card from '../../shared/Card'
import Button from '../../shared/Button'
import TextInput from '../../shared/TextInput'
import Spinner from '../../shared/Spinner'
import EmptyState from '../../shared/EmptyState'
import QuestionList from './QuestionList'
import * as ChecklistService from '../../services/ChecklistService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'
import type { useChecklist } from '../../hooks/useChecklist'

function CategoryEditor() {
  const { categoryId } = useParams<{ categoryId: string }>()
  const checklist = useOutletContext<ReturnType<typeof useChecklist>>()
  const navigate = useNavigate()
  const { showToast } = useToast()
  const category = checklist.categories.find((c) => c.id === categoryId)

  const [name, setName] = useState(category?.name ?? '')
  const [busy, setBusy] = useState(false)
  const [confirmingDelete, setConfirmingDelete] = useState(false)

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- resets the local form when the selected category changes
    setName(category?.name ?? '')
    setConfirmingDelete(false)
  }, [category?.id, category?.name])

  if (!category) {
    return <EmptyState title="Category not found" description="It may have been deleted." />
  }

  async function handleSave() {
    setBusy(true)
    try {
      await ChecklistService.patchCategory(category!.id, { name: name.trim() })
      showToast({ kind: 'info', message: 'Category saved' })
      await checklist.refresh()
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to save category' })
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
      await ChecklistService.deleteCategory(category!.id)
      showToast({ kind: 'info', message: `Deleted ${category!.name}` })
      await checklist.refresh()
      navigate('/checklist')
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to delete category' })
    } finally {
      setBusy(false)
      setConfirmingDelete(false)
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <TextInput value={name} onChange={setName} placeholder="Category name" />
        <div className="mt-4 flex items-center gap-3">
          <Button onClick={handleSave} disabled={busy || !name.trim() || name.trim() === category.name}>
            {busy ? <Spinner /> : 'Save name'}
          </Button>
          <Button variant="ghost" onClick={handleDelete} disabled={busy}>
            {confirmingDelete ? 'Confirm delete' : 'Delete category'}
          </Button>
        </div>
      </Card>
      <QuestionList category={category} onChanged={checklist.refresh} />
    </div>
  )
}

export default CategoryEditor
