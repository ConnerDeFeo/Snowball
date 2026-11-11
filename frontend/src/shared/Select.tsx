interface Option {
  value: string
  label: string
}

interface SelectProps {
  value: string
  onChange: (value: string) => void
  options: Option[]
  disabled?: boolean
  compact?: boolean
}

function Select({ value, onChange, options, disabled, compact }: SelectProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      disabled={disabled}
      className={`w-full rounded-lg border border-secondary-ice bg-primary text-slate-800 focus:border-secondary focus:ring-2 focus:ring-secondary/50 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50 ${
        compact ? 'px-2 py-1 text-sm' : 'px-4 py-2.5'
      }`}
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  )
}

export default Select
