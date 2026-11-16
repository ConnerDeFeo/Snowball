import { useState } from 'react'
import Card from '../../shared/Card'
import Tabs from '../../shared/Tabs'
import { TRADE_CODES, TRADE_FILTER_OPTIONS, codeLabel, type TradeFilter } from '../../constants/insiders'
import type { InsiderFiling } from '../../services/types/InsidersTypes'

interface TransactionsTableProps {
  filings: InsiderFiling[]
  onSelect: (filingId: string) => void
}

const HEADERS = ['Date', 'Insider', 'Position', 'Code', 'Shares', 'Price', 'Value', 'Owned after']

const num = (n: number | null, digits = 0) =>
  n === null ? '' : n.toLocaleString('en-US', { maximumFractionDigits: digits })

function TransactionsTable({ filings, onSelect }: TransactionsTableProps) {
  const [filter, setFilter] = useState<TradeFilter>('all')

  // Each row remembers its filing so a click can open the document.
  const rows = filings
    .flatMap((f) => f.transactions.map((t) => ({ filingId: f.id, ...t })))
    .filter((t) => filter === 'all' || TRADE_CODES.includes(t.code))

  return (
    <Card>
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-800">Insider transactions</h2>
        <Tabs options={TRADE_FILTER_OPTIONS} value={filter} onChange={setFilter} />
      </div>
      {rows.length === 0 ? (
        <p className="text-sm text-slate-500">No transactions in this range.</p>
      ) : (
        <div className="max-h-80 overflow-auto">
          <table className="w-full border-collapse text-sm">
            <thead className="sticky top-0 bg-white">
              <tr className="border-b border-secondary-ice text-left text-xs uppercase tracking-wide text-slate-400">
                {HEADERS.map((h, i) => (
                  <th key={h} className={`whitespace-nowrap px-3 py-2 font-semibold ${i >= 4 ? 'text-right' : ''}`}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((t, i) => (
                <tr
                  key={i}
                  onClick={() => onSelect(t.filingId)}
                  className="cursor-pointer border-b border-secondary-ice/60 hover:bg-secondary-ice/40"
                >
                  <td className="whitespace-nowrap px-3 py-1.5 text-slate-700">{t.date}</td>
                  <td className="px-3 py-1.5 text-slate-800">{t.insider}</td>
                  <td className="px-3 py-1.5 text-slate-700">{t.position}</td>
                  <td className="whitespace-nowrap px-3 py-1.5 text-slate-700">{codeLabel(t.code)}</td>
                  <td className="px-3 py-1.5 text-right tabular-nums">{num(t.shares)}</td>
                  <td className="px-3 py-1.5 text-right tabular-nums">{num(t.price, 2)}</td>
                  <td className="px-3 py-1.5 text-right tabular-nums">{num(t.value)}</td>
                  <td className="px-3 py-1.5 text-right tabular-nums">{num(t.remaining)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  )
}

export default TransactionsTable
