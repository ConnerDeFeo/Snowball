interface CheckboxProps {
  checked: boolean
  onChange: (checked: boolean) => void
  label: string
}

function Checkbox({ checked, onChange, label }: CheckboxProps) {
  return (
    <label className="flex cursor-pointer items-center gap-2 text-sm text-slate-600">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="h-4 w-4 accent-secondary-deep"
      />
      {label}
    </label>
  )
}

export default Checkbox
