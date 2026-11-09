import { useState } from 'react'
import Card from '../../shared/Card'
import EmptyState from '../../shared/EmptyState'
import Select from '../../shared/Select'
import Tabs from '../../shared/Tabs'
import StatementTable from './StatementTable'
import { STATEMENTS } from '../../constants/statements'
import type { FilingStatements, StatementKey } from '../../services/types/FinancialsTypes'

interface FinancialsViewProps {
  filings: FilingStatements[]
  loading: boolean
  error: string | null
  onRetry: () => void
}

function filingId(f: FilingStatements): string {
  return `${f.form}-${f.year}-${f.quarter ?? ''}`
}

function filingLabel(f: FilingStatements): string {
  return f.quarter ? `${f.form} ${f.year} ${f.quarter}` : `${f.form} FY${f.year}`
}

function FinancialsView({ filings, loading, error, onRetry }: FinancialsViewProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [statementKey, setStatementKey] = useState<StatementKey>('income')

  if (loading && filings.length === 0) {
    return <div className="h-64 animate-pulse rounded-2xl bg-secondary-ice" />
  }
  if (error) {
    return (
      <EmptyState
        title="Couldn't load financial statements"
        description={error}
        action={
          <button onClick={onRetry} className="text-sm font-semibold text-secondary-deep underline">
            Retry
          </button>
        }
      />
    )
  }
  if (filings.length === 0) {
    return <EmptyState title="No financial statements yet" description="Fetch filings for this year range to see them here." />
  }

  const filing = filings.find((f) => filingId(f) === selectedId) ?? filings[0]
  const statement = filing.statements[statementKey]

  return (
    <Card>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <Tabs options={STATEMENTS} value={statementKey} onChange={setStatementKey} />
        <div className="w-56">
          <Select
            value={filingId(filing)}
            onChange={setSelectedId}
            options={filings.map((f) => ({ value: filingId(f), label: filingLabel(f) }))}
          />
        </div>
      </div>
      <div className="mt-4">
        {statement ? (
          <StatementTable statement={statement} />
        ) : (
          <p className="text-sm text-slate-500">This filing has no {STATEMENTS.find((s) => s.value === statementKey)?.label.toLowerCase()} data.</p>
        )}
      </div>
    </Card>
  )
}

export default FinancialsView
