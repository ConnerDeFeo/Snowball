from enum import Enum

class RubricCategory(Enum):
    REVENUE_DURABILITY = "Revenue durability"
    REVENUE_QUALITY = "Revenue quality"
    CUSTOMER_CONCENTRATION = "Customer concentration"
    SUPPLIER_CONCENTRATION = "Supplier concentration"
    GROSS_MARGIN = "Gross margin level"
    GROSS_MARGIN_STABILITY = "Gross margin stability"
    MOAT = "Competitive moat / ROIC persistence"
    CAPITAL_BURDENS = "Capital intensity & reinvestment burden"
    EARNINGS_QUALITY = "Earnings quality / cash conversion"
    MANAGEMENT = "Management"
    CAP_ALLOC = "Capital allocation"
    BALANCE_SHEET = "Balance sheet resilience"
    INDUSTRY_STRUCT = "Industry structure"
    ACCOUNTING_STANDARDS = "Accounting standards"
