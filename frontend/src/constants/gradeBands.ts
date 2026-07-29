import type { GradedTimePeriod } from '../services/types/GradingTypes'

export type GradeBand = 'strong' | 'mixed' | 'weak' | 'none'

const BAND_CLASSES: Record<GradeBand, string> = {
  strong: 'bg-emerald-50 text-emerald-700 border border-emerald-200',
  mixed: 'bg-amber-50 text-amber-700 border border-amber-200',
  weak: 'bg-rose-50 text-rose-700 border border-rose-200',
  none: 'bg-slate-100 text-slate-500 border border-slate-200',
}

export function isNoEvidence(g: GradedTimePeriod): boolean {
  return g.grade === 0 && /no evidence/i.test(g.reasoning)
}

export function gradeBand(g: GradedTimePeriod): GradeBand {
  if (isNoEvidence(g)) return 'none'
  if (g.grade >= 70) return 'strong'
  if (g.grade >= 40) return 'mixed'
  return 'weak'
}

export function gradeBandClasses(band: GradeBand): string {
  return BAND_CLASSES[band]
}
