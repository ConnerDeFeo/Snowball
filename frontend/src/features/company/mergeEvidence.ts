import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

// Results from runs in this tab (applied in order) take priority over stored
// evidence, since they're guaranteed fresher than whatever the read route last
// saw. Merges at question granularity so a one-question run only replaces that
// question and leaves the category's other questions alone.
export function mergeEvidence(server: EvidenceCategory[], session: EvidenceCategory[]): EvidenceCategory[] {
  const result = server.map((c) => ({ ...c, questions: [...c.questions] }))
  for (const s of session) {
    const target = result.find((c) => c.id === s.id)
    if (!target) {
      result.push({ ...s, questions: [...s.questions] })
      continue
    }
    target.name = s.name
    for (const q of s.questions) {
      const i = target.questions.findIndex((t) => t.id === q.id)
      if (i === -1) target.questions.push(q)
      else target.questions[i] = q
    }
  }
  return result
}
