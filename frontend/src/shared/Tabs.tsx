interface Option<T extends string> {
  value: T
  label: string
}

interface TabsProps<T extends string> {
  options: readonly Option<T>[]
  value: T
  onChange: (value: T) => void
}

function Tabs<T extends string>({ options, value, onChange }: TabsProps<T>) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => onChange(opt.value)}
          className={`cursor-pointer rounded-lg px-4 py-2 text-sm font-semibold transition-colors ${
            opt.value === value ? 'bg-secondary text-white' : 'text-slate-500 hover:bg-secondary-ice'
          }`}
        >
          {opt.label}
        </button>
      ))}
    </div>
  )
}

export default Tabs
