const STATUS_CLASSES: Record<string, string> = {
  disclosed: 'bg-emerald-50 text-emerald-700 border border-emerald-200',
  not_disclosed: 'bg-slate-100 text-slate-500 border border-slate-200',
}

export function statusClasses(status: string): string {
  return STATUS_CLASSES[status] ?? STATUS_CLASSES.not_disclosed
}

// Answered-count badge: all answered = green, some = amber, none = grey.
export function answeredClasses(answered: number, total: number): string {
  if (total > 0 && answered === total) return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
  if (answered > 0) return 'bg-amber-50 text-amber-700 border border-amber-200'
  return 'bg-slate-100 text-slate-500 border border-slate-200'
}
