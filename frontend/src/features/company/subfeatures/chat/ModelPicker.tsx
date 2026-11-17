import { useState } from 'react'
import { CHAT_EFFORTS, CHAT_MODELS } from '../../../../constants/chatModels'
import type { ChatEffort, ChatModel } from '../../../../constants/chatModels'

interface Option {
  value: string
  label: string
}

interface ModelPickerProps {
  model: ChatModel
  effort: ChatEffort
  onModelChange: (model: ChatModel) => void
  onEffortChange: (effort: ChatEffort) => void
  disabled?: boolean
}

interface GroupProps {
  title: string
  options: readonly Option[]
  value: string
  onPick: (value: string) => void
}

function Group({ title, options, value, onPick }: GroupProps) {
  return (
    <div>
      <p className="px-2 pt-1 text-[10px] font-semibold tracking-wide text-slate-400 uppercase">{title}</p>
      {options.map((o) => (
        <button
          key={o.value}
          onClick={() => onPick(o.value)}
          className={`block w-full cursor-pointer rounded-md px-2 py-1 text-left text-xs text-slate-700 hover:bg-secondary-ice ${
            o.value === value ? 'bg-secondary-ice font-medium' : ''
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  )
}

// Small "[model] [effort]" chip; click opens an upward dropdown to change either.
function ModelPicker({ model, effort, onModelChange, onEffortChange, disabled }: ModelPickerProps) {
  const [open, setOpen] = useState(false)
  const modelLabel = CHAT_MODELS.find((m) => m.value === model)?.label
  const effortLabel = CHAT_EFFORTS.find((e) => e.value === effort)?.label

  return (
    <div className="relative">
      {open && <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />}
      {open && (
        <div className="absolute right-0 bottom-full z-20 mb-2 w-36 rounded-xl border border-secondary-ice bg-white p-1 shadow-lg">
          <Group title="Model" options={CHAT_MODELS} value={model} onPick={(v) => onModelChange(v as ChatModel)} />
          <Group title="Effort" options={CHAT_EFFORTS} value={effort} onPick={(v) => onEffortChange(v as ChatEffort)} />
        </div>
      )}
      <button
        onClick={() => setOpen((o) => !o)}
        disabled={disabled}
        title="Model and thinking effort"
        className="cursor-pointer rounded-full border border-secondary-ice px-2.5 py-1 text-xs text-slate-600 hover:bg-secondary-ice disabled:cursor-not-allowed disabled:opacity-50"
      >
        {modelLabel} · {effortLabel}
      </button>
    </div>
  )
}

export default ModelPicker
