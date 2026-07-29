import type { GradedTimePeriod } from '../../services/types/GradingTypes'

// Session grades (from a run in this tab) take priority over server grades,
// since they're guaranteed fresher than whatever the read route last saw.
export function mergeGrades(
  serverGrades: GradedTimePeriod[],
  sessionGrades: GradedTimePeriod[],
): Map<string, GradedTimePeriod> {
  const map = new Map<string, GradedTimePeriod>()
  for (const g of serverGrades) map.set(g.category, g)
  for (const g of sessionGrades) map.set(g.category, g)
  return map
}
