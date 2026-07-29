interface TextInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

function TextInput({ value, onChange, placeholder }: TextInputProps) {
  return (
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full rounded-lg border border-secondary-ice bg-primary px-4 py-2.5 text-slate-800 placeholder:text-slate-400 focus:border-secondary focus:ring-2 focus:ring-secondary/50 focus:outline-none"
    />
  )
}

export default TextInput
