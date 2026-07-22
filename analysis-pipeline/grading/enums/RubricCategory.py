from enum import Enum

from enum import Enum

class RubricCategory(Enum):
    REVENUE_DURABILITY = "revenue_durability"
    REVENUE_QUALITY = "revenue_quality"
    CUSTOMER_CONCENTRATION = "customer_concentration"
    SUPPLIER_CONCENTRATION = "supplier_concentration"
    GROSS_MARGIN = "gross_margin_level"
    GROSS_MARGIN_STABILITY = "gross_margin_stability"
    MOAT = "competitive_moat_roic_persistence"
    CAPITAL_BURDENS = "capital_intensity_reinvestment_burden"
    EARNINGS_QUALITY = "earnings_quality_cash_conversion"
    MANAGEMENT = "management"
    CAP_ALLOC = "capital_allocation"
    BALANCE_SHEET = "balance_sheet_resilience"
    INDUSTRY_STRUCT = "industry_structure"
    ACCOUNTING_STANDARDS = "accounting_standards"

    @property
    def display(self) -> str:
        return self.value.replace("_", " ").capitalize()