interface EmptyStateProps {
  title: string
  description?: string
  action?: React.ReactNode
}

function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-2xl border border-secondary-ice bg-white/50 p-10 text-center">
      <span className="text-3xl text-secondary-deep">❄</span>
      <p className="text-lg font-semibold text-slate-800">{title}</p>
      {description && <p className="max-w-sm text-sm text-slate-500">{description}</p>}
      {action}
    </div>
  )
}

export default EmptyState
