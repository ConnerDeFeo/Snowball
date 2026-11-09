import type { EvidenceCategory, EvidenceQuestion } from '../../services/types/EvidenceTypes'

// A question counts as answered once any sub-agent has found at least one finding.
export function isAnswered(question: EvidenceQuestion): boolean {
  return question.sub_agents.some((sa) => sa.evidence.some((e) => e.findings.length > 0))
}

export function countAnswered(category: EvidenceCategory): number {
  return category.questions.filter(isAnswered).length
}

// Number of filings any sub-agent has evidence for.
export function filingCount(question: EvidenceQuestion): number {
  return question.sub_agents.reduce((sum, sa) => sum + sa.evidence.length, 0)
}
