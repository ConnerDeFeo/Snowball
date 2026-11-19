import { useState } from 'react'
import Card from '../../shared/Card'
import EmptyState from '../../shared/EmptyState'
import Select from '../../shared/Select'
import Spinner from '../../shared/Spinner'
import ProxySummary from './ProxySummary'
import YearlyTable from './YearlyTable'
import { EXEC_COMP_COLUMNS, PAY_VS_PERFORMANCE_COLUMNS } from '../../constants/proxies'
import type { ProxyColumn } from '../../constants/proxies'
import type { ProxyFiling, ProxyRecord } from '../../services/types/ProxyTypes'

interface ProxiesViewProps {
  filings: ProxyFiling[]
  loading: boolean
  error: string | null
  onRetry: () => void
  fetching: boolean
}

// Named executive rows have no fixed shape, so columns come from the first row's keys.
function columnsFor(rows: ProxyRecord[] | null): ProxyColumn[] {
  return Object.keys(rows?.[0] ?? {}).map((key) => ({ key, label: key.replace(/_/g, ' '), kind: 'number' }))
}

function ProxiesView({ filings, loading, error, onRetry, fetching }: ProxiesViewProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)

  if (loading && filings.length === 0) {
    return <div className="h-64 animate-pulse rounded-2xl bg-secondary-ice" />
  }
  if (error) {
    return (
      <EmptyState
        title="Couldn't load proxy statements"
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
    return (
      <EmptyState
        title="No proxy statements yet"
        description="Fetch filings for this year range to see them here."
        action={
          fetching && (
            <span className="flex items-center gap-2 text-sm text-slate-500"><Spinner /> Fetching filings…</span>
          )
        }
      />
    )
  }

  const filing = filings.find((f) => f.id === selectedId) ?? filings[0]
  const { data } = filing
  const named = data.executive_compensation.named_executives

  return (
    <Card>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-secondary-deep">{data.metadata.company_name ?? 'Proxy statement'}</h2>
          <p className="text-xs text-slate-500">
            {data.metadata.form} filed {data.metadata.filing_date ?? '—'} · {data.metadata.accession_number ?? '—'}
          </p>
        </div>
        <div className="w-48">
          <Select
            value={filing.id}
            onChange={setSelectedId}
            options={filings.map((f) => ({ value: f.id, label: `Filed ${f.filing_date}` }))}
          />
        </div>
      </div>
      <ProxySummary data={data} />
      <YearlyTable title="Executive compensation" columns={EXEC_COMP_COLUMNS} rows={data.executive_compensation.executive_compensation} />
      <YearlyTable title="Pay versus performance" columns={PAY_VS_PERFORMANCE_COLUMNS} rows={data.pay_vs_performance.pay_vs_performance} />
      <YearlyTable title="Named executives" columns={columnsFor(named)} rows={named} />
    </Card>
  )
}

export default ProxiesView
