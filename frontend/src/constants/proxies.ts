export type ColumnKind = 'text' | 'usd' | 'number'

export interface ProxyColumn {
  key: string
  label: string
  kind: ColumnKind
}

export const EXEC_COMP_COLUMNS: ProxyColumn[] = [
  { key: 'fiscal_year_end', label: 'Fiscal year end', kind: 'text' },
  { key: 'peo_total_comp', label: 'PEO total', kind: 'usd' },
  { key: 'peo_actually_paid_comp', label: 'PEO actually paid', kind: 'usd' },
  { key: 'neo_avg_total_comp', label: 'Other NEOs avg total', kind: 'usd' },
  { key: 'neo_avg_actually_paid_comp', label: 'Other NEOs avg paid', kind: 'usd' },
]

export const PAY_VS_PERFORMANCE_COLUMNS: ProxyColumn[] = [
  { key: 'fiscal_year_end', label: 'Fiscal year end', kind: 'text' },
  { key: 'peo_actually_paid_comp', label: 'PEO actually paid', kind: 'usd' },
  { key: 'neo_avg_actually_paid_comp', label: 'Other NEOs avg paid', kind: 'usd' },
  { key: 'total_shareholder_return', label: 'TSR (value of $100)', kind: 'number' },
  { key: 'net_income', label: 'Net income', kind: 'usd' },
  { key: 'company_selected_measure_value', label: 'Selected measure', kind: 'usd' },
]
