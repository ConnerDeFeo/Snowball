import { useState } from 'react'
import EvidenceItemView from './EvidenceItemView'
import { filingCount } from './evidenceStats'
import { displaySection } from '../../constants/categories'
import type { Section } from '../../enums/Sections'
import type { EvidenceQuestion } from '../../services/types/EvidenceTypes'

interface QuestionRowProps {
  question: EvidenceQuestion
  disabled: boolean
  onRun: () => void
}

function QuestionRow({ question, disabled, onRun }: QuestionRowProps) {
  const [open, setOpen] = useState(false)
  const filings = filingCount(question)

  return (
    <li className="group rounded-lg border border-secondary-ice">
      <div className="flex items-center justify-between gap-3 p-3">
        <button onClick={() => setOpen(!open)} className="flex flex-1 cursor-pointer items-start gap-2 text-left">
          <span className="mt-0.5 text-xs text-slate-400">{open ? '▾' : '▸'}</span>
          <span>
            <span className="text-sm font-medium text-slate-800">{question.text}</span>
            <span className="ml-2 text-xs text-slate-400">
              {filings === 0 ? 'no evidence yet' : `${filings} filing${filings === 1 ? '' : 's'}`}
              {` · ${question.form} · ${displaySection(question.section as Section)}`}
              {question.latest_only && ' · latest only'}
            </span>
          </span>
        </button>
        <button
          onClick={onRun}
          disabled={disabled}
          title="Run this question"
          className="cursor-pointer text-lg text-secondary-deep opacity-0 transition-opacity group-hover:opacity-100 focus:opacity-100 disabled:cursor-not-allowed disabled:opacity-30"
        >
          ↻
        </button>
      </div>

      {open && (
        <div className="flex flex-col gap-3 border-t border-secondary-ice p-3">
          {question.evidence.length === 0 ? (
            <p className="text-sm text-slate-500">Not run yet.</p>
          ) : (
            question.evidence.map((item) => <EvidenceItemView key={`${item.year}-${item.quarter}`} item={item} />)
          )}
        </div>
      )}
    </li>
  )
}

export default QuestionRow
