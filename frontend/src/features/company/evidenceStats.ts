import type { EvidenceCategory, EvidenceQuestion } from '../../services/types/EvidenceTypes'

// A question counts as answered once any filing has at least one finding.
export function isAnswered(question: EvidenceQuestion): boolean {
  return question.evidence.some((e) => e.findings.length > 0)
}

export function countAnswered(category: EvidenceCategory): number {
  return category.questions.filter(isAnswered).length
}

// Number of filings the question has evidence for.
export function filingCount(question: EvidenceQuestion): number {
  return question.evidence.length
}
