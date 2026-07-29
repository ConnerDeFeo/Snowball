interface TextAreaProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  rows?: number
  onKeyDown?: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void
  disabled?: boolean
}

function TextArea({ value, onChange, placeholder, rows = 4, onKeyDown, disabled }: TextAreaProps) {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      rows={rows}
      onKeyDown={onKeyDown}
      disabled={disabled}
      className="w-full rounded-lg border border-secondary-ice bg-primary px-4 py-2.5 text-slate-800 placeholder:text-slate-400 focus:border-secondary focus:ring-2 focus:ring-secondary/50 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
    />
  )
}

export default TextArea
