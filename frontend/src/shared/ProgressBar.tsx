interface ProgressBarProps {
  completed: number
  total: number
  label?: string
}

function ProgressBar({ completed, total, label }: ProgressBarProps) {
  const pct = total > 0 ? Math.min(100, Math.round((completed / total) * 100)) : 0
  return (
    <div className="w-full">
      {label && <p className="mb-1.5 text-sm text-slate-500">{label}</p>}
      <div className="h-2 w-full overflow-hidden rounded-full bg-secondary-ice">
        <div
          className="h-full rounded-full bg-secondary-deep transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

export default ProgressBar
