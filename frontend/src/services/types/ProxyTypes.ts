export type ProxyRecord = Record<string, string | number | boolean | null>

export interface ProxyData {
  metadata: {
    form: string | null
    filing_date: string | null
    company_name: string | null
    accession_number: string | null
  }
  executive_compensation: {
    peo_name: string | null
    peo_total_comp: number | null
    peo_actually_paid_comp: number | null
    neo_avg_total_comp: number | null
    neo_avg_actually_paid_comp: number | null
    executive_compensation: ProxyRecord[] | null
    named_executives: ProxyRecord[] | null
  }
  pay_vs_performance: {
    total_shareholder_return: number | null
    net_income: number | null
    company_selected_measure: string | null
    company_selected_measure_value: number | null
    pay_vs_performance: ProxyRecord[] | null
  }
  governance: {
    insider_trading_policy_adopted: boolean | null
  }
}

export interface ProxyFiling {
  id: string
  filing_date: string
  data: ProxyData
}
