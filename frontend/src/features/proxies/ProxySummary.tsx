import { formatUsd } from './formatProxy'
import type { ProxyData } from '../../services/types/ProxyTypes'

interface TileProps {
  label: string
  value: string
}

function Tile({ label, value }: TileProps) {
  return (
    <div className="rounded-xl border border-secondary-ice bg-white/60 p-4">
      <p className="text-xs uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-1 text-lg font-semibold tabular-nums text-secondary-deep">{value}</p>
    </div>
  )
}

function policyLabel(adopted: boolean | null): string {
  if (adopted == null) return '—'
  return adopted ? 'Adopted' : 'Not adopted'
}

function ProxySummary({ data }: { data: ProxyData }) {
  const comp = data.executive_compensation
  const perf = data.pay_vs_performance
  return (
    <div className="mt-4 grid grid-cols-2 gap-3 lg:grid-cols-3">
      <Tile label="PEO" value={comp.peo_name ?? '—'} />
      <Tile label="PEO total comp" value={formatUsd(comp.peo_total_comp)} />
      <Tile label="PEO actually paid" value={formatUsd(comp.peo_actually_paid_comp)} />
      <Tile label="Other NEOs avg total" value={formatUsd(comp.neo_avg_total_comp)} />
      <Tile label="Other NEOs avg paid" value={formatUsd(comp.neo_avg_actually_paid_comp)} />
      <Tile label="TSR (value of $100)" value={perf.total_shareholder_return?.toString() ?? '—'} />
      <Tile label="Net income" value={formatUsd(perf.net_income)} />
      <Tile label={perf.company_selected_measure ?? 'Selected measure'} value={formatUsd(perf.company_selected_measure_value)} />
      <Tile label="Insider trading policy" value={policyLabel(data.governance.insider_trading_policy_adopted)} />
    </div>
  )
}

export default ProxySummary
