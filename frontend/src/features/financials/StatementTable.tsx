import { formatValue } from './formatValue'
import { periodColumns } from './periodColumns'
import type { Statement } from '../../services/types/FinancialsTypes'

interface StatementTableProps {
  statement: Statement
}

const INDENT_REM = 1

function StatementTable({ statement: raw }: StatementTableProps) {
  const statement = periodColumns(raw)
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-secondary-ice text-left text-xs uppercase tracking-wide text-slate-400">
            <th className="py-2 pr-4 font-semibold">USD in millions, except per-share</th>
            {statement.columns.map((column) => (
              <th key={column} className="whitespace-nowrap px-3 py-2 text-right font-semibold">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {statement.rows.map((row, i) => (
            <tr key={i} className="border-b border-secondary-ice/60">
              <td
                className={`py-1.5 pr-4 ${row.abstract ? 'font-semibold text-slate-800' : 'text-slate-700'}`}
                style={{ paddingLeft: `${row.level * INDENT_REM}rem` }}
              >
                {row.label}
              </td>
              {row.values.map((value, j) => (
                <td key={j} className="whitespace-nowrap px-3 py-1.5 text-right tabular-nums text-slate-800">
                  {row.abstract ? '' : formatValue(value, row.unit)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default StatementTable
