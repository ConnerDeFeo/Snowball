import { useState } from 'react'
import Button from '../../shared/Button'
import Spinner from '../../shared/Spinner'
import TextInput from '../../shared/TextInput'
import * as ChecklistService from '../../services/ChecklistService'
import { ApiError } from '../../services/API'
import { useToast } from '../../hooks/useToast'

interface AddCategoryFormProps {
  nextOrder: number
  onCreated: (categoryId: string) => void
}

function AddCategoryForm({ nextOrder, onCreated }: AddCategoryFormProps) {
  const { showToast } = useToast()
  const [name, setName] = useState('')
  const [busy, setBusy] = useState(false)

  async function handleAdd() {
    setBusy(true)
    try {
      const { id } = await ChecklistService.createCategory({ name: name.trim(), order: nextOrder })
      setName('')
      onCreated(id)
    } catch (err) {
      showToast({ kind: 'error', message: err instanceof ApiError ? err.detail : 'Failed to create category' })
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="mt-3 flex flex-col gap-2 border-t border-secondary-ice pt-3">
      <TextInput value={name} onChange={setName} placeholder="New category name" />
      <Button variant="ghost" onClick={handleAdd} disabled={busy || !name.trim()}>
        {busy ? <Spinner /> : 'Add category'}
      </Button>
    </div>
  )
}

export default AddCategoryForm
