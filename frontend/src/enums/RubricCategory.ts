export const RUBRIC_CATEGORIES = [
  'revenue_durability',
  'revenue_quality',
  'customer_concentration',
  'supplier_concentration',
  'gross_margin_level',
  'gross_margin_stability',
  'competitive_moat_roic_persistence',
  'capital_intensity_reinvestment_burden',
  'earnings_quality_cash_conversion',
  'management',
  'capital_allocation',
  'balance_sheet_resilience',
  'industry_structure',
  'accounting_standards',
] as const

export type RubricCategory = (typeof RUBRIC_CATEGORIES)[number]
