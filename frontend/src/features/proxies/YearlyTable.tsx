import { formatCell } from './formatProxy'
import type { ProxyColumn } from '../../constants/proxies'
import type { ProxyRecord } from '../../services/types/ProxyTypes'

interface YearlyTableProps {
  title: string
  columns: ProxyColumn[]
  rows: ProxyRecord[] | null
}

function YearlyTable({ title, columns, rows }: YearlyTableProps) {
  if (!rows || rows.length === 0) return null
  return (
    <div className="mt-6">
      <h3 className="mb-2 text-sm font-semibold text-secondary-deep">{title}</h3>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-secondary-ice text-left text-xs uppercase tracking-wide text-slate-400">
              {columns.map((c, i) => (
                <th key={c.key} className={`whitespace-nowrap px-3 py-2 font-semibold ${i === 0 ? 'pl-0' : 'text-right'}`}>
                  {c.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i} className="border-b border-secondary-ice/60">
                {columns.map((c, j) => (
                  <td
                    key={c.key}
                    className={`whitespace-nowrap px-3 py-1.5 text-slate-800 ${j === 0 ? 'pl-0' : 'text-right tabular-nums'}`}
                  >
                    {formatCell(row[c.key], c.kind)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default YearlyTable
