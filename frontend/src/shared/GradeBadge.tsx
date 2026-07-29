import { gradeBand, gradeBandClasses, isNoEvidence } from '../constants/gradeBands'
import type { GradedTimePeriod } from '../services/types/GradingTypes'

interface GradeBadgeProps {
  graded?: GradedTimePeriod
}

function GradeBadge({ graded }: GradeBadgeProps) {
  if (!graded) {
    return (
      <span className={`inline-block rounded-full px-3 py-1 text-sm font-semibold ${gradeBandClasses('none')}`}>
        Not graded
      </span>
    )
  }

  const band = gradeBand(graded)
  const label = isNoEvidence(graded) ? 'No evidence' : Math.round(graded.grade)

  return (
    <span className={`inline-block rounded-full px-3 py-1 text-sm font-semibold ${gradeBandClasses(band)}`}>
      {label}
    </span>
  )
}

export default GradeBadge
