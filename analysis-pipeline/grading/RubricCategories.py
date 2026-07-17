from enum import Enum
from TenKSections import TenKSection
from TenQSections import TenQSection

### THIS IS A STANDIN FOR NOW, FURTHER RESEARCH WILL BE DONE EXTENSIVLEY LATER ON ALL AREAS
### Proxy-only source material (exec bios, CD&A) is mapped to the closest 10-K item
### (Item 10 / Item 11), since the 10-K frequently incorporates it by reference and
### there's no dedicated proxy section enum yet.

class RubricCategories(Enum):
    REVENUE_DURABILITY = {
        "name": "Revenue durability",
        "locations": [
            TenKSection.PART_I_ITEM_1,      # Business - contract structure, recurring vs. project-based revenue, backlog
            TenKSection.PART_II_ITEM_7,     # MD&A - revenue drivers and disaggregation discussion
            TenKSection.PART_II_ITEM_8,     # Notes - Revenue Recognition footnote (ASC 606 disaggregation)
        ],
        "directions": "Determine what share of revenue is contractual, recurring, or subscription-based versus one-time or project-based, and how much visibility management has into future revenue (backlog, deferred revenue, remaining performance obligations).",
    }
    REVENUE_QUALITY = {
        "name": "Revenue quality",
        "locations": [
            TenKSection.PART_II_ITEM_7,     # MD&A - discussion of one-time items, divestiture gains, or channel stuffing risk
            TenKSection.PART_II_ITEM_8,     # Notes - Revenue Recognition footnote (timing of recognition, contract assets/liabilities)
            TenQSection.PART_I_ITEM_1,      # Financial Statements - quarter-over-quarter revenue trend and any restatements
            TenQSection.PART_I_ITEM_2,      # MD&A - quarterly commentary on revenue trend
        ],
        "directions": "Assess whether reported revenue reflects real cash-backed demand versus aggressive recognition timing, non-recurring gains, or channel-stuffing, using the recognition footnote and any MD&A caveats.",
    }
    # CUSTOMER_CONCENTRATION = {
    #     "name": "Customer concentration",
    #     "locations": [
    #         TenKSection.PART_I_ITEM_1,      # Business - major customers disclosure (any customer >10% of revenue)
    #         TenKSection.PART_I_ITEM_1A,     # Risk Factors - customer dependency risk language
    #         TenKSection.PART_II_ITEM_8,     # Notes - segment/customer concentration footnote
    #     ],
    #     "directions": "Identify whether revenue is concentrated in a small number of customers and note any disclosed loss-of-customer risk, contract renewal terms, or dependency language that signals fragility.",
    # }
    # SUPPLIER_CONCENTRATION = {
    #     "name": "Supplier concentration",
    #     "locations": [
    #         TenKSection.PART_I_ITEM_1,      # Business - supply chain and sourcing description
    #         TenKSection.PART_I_ITEM_1A,     # Risk Factors - single-source or key supplier dependency risk
    #         TenKSection.PART_II_ITEM_7,     # MD&A - commentary on input cost or supply disruption
    #     ],
    #     "directions": "Determine how dependent the company is on a limited number of suppliers or single-source components, and whether management discloses substitutability or long-term supply agreements that mitigate that risk.",
    # }
    # GROSS_MARGIN = {
    #     "name": "Gross margin level",
    #     "locations": [
    #         TenKSection.PART_II_ITEM_7,     # MD&A - gross margin discussion and drivers
    #         TenKSection.PART_II_ITEM_8,     # Financial Statements / Notes - gross profit line and segment margin footnote
    #         TenQSection.PART_I_ITEM_1,      # Financial Statements - gross profit line
    #     ],
    #     "directions": "Record the current gross margin level and compare it against segment or product-line detail to see whether the reported figure is being propped up or dragged down by a particular business line.",
    # }
    # GROSS_MARGIN_STABILITY = {
    #     "name": "Gross margin stability",
    #     "locations": [
    #         TenKSection.PART_II_ITEM_7,     # MD&A - multi-year margin trend commentary
    #         TenKSection.PART_II_ITEM_8,     # Notes - pricing, input cost, or mix-shift discussion affecting margin
    #         TenQSection.PART_I_ITEM_1,      # Financial Statements - quarter-over-quarter margin trend
    #         TenQSection.PART_I_ITEM_2,      # MD&A - quarterly margin commentary
    #     ],
    #     "directions": "Track gross margin across recent quarters and years to assess volatility, and read management's explanation for swings (pricing power, input costs, product mix) to judge whether the margin is structurally stable.",
    # }
    # MOAT = {
    #     "name": "Competitive moat / ROIC persistence",
    #     "locations": [
    #         TenKSection.PART_I_ITEM_1,      # Business - competitive strengths / competitive advantages section
    #         TenKSection.PART_I_ITEM_1A,     # Risk Factors - competition risk language
    #         TenKSection.PART_II_ITEM_7,     # MD&A - historical returns/operating income trend commentary
    #         TenKSection.PART_II_ITEM_8,     # Financial Statements - operating income, invested capital inputs (multi-year)
    #     ],
    #     "directions": "Evaluate management's stated competitive advantages against historical evidence of sustained high returns on invested capital, since a durable moat should show up as persistence rather than a single strong year.",
    # }
    # CAPITAL_BURDENS = {
    #     "name": "Capital intensity & reinvestment burden",
    #     "locations": [
    #         TenKSection.PART_II_ITEM_7,     # MD&A - Liquidity and Capital Resources section
    #         TenKSection.PART_II_ITEM_8,     # Cash Flow Statement / Notes - capex line, PP&E footnote
    #         TenQSection.PART_I_ITEM_1,      # Cash Flow Statement - capital expenditures line
    #     ],
    #     "directions": "Compare capex to revenue and operating cash flow to gauge how much of earnings must be reinvested just to maintain the business, distinguishing maintenance capex from growth capex where disclosed.",
    # }
    # EARNINGS_QUALITY = {
    #     "name": "Earnings quality / cash conversion",
    #     "locations": [
    #         TenKSection.PART_II_ITEM_7,     # MD&A - non-GAAP reconciliation and adjustments discussion
    #         TenKSection.PART_II_ITEM_8,     # Cash Flow Statement / Notes - reconciliation of net income to operating cash flow, reserves/accruals footnotes
    #         TenQSection.PART_I_ITEM_1,      # Cash Flow Statement - net income to operating cash flow reconciliation
    #     ],
    #     "directions": "Check how closely net income converts into operating cash flow over time, and scan for large or growing gaps driven by accruals, reserve releases, or non-GAAP adjustments that could flatter reported earnings.",
    # }
    # MANAGEMENT = {
    #     "name": "Management",
    #     "locations": [
    #         TenKSection.PART_III_ITEM_10,   # Directors, Executive Officers, Corporate Governance - bios (often by reference to proxy)
    #         TenKSection.PART_III_ITEM_11,   # Executive Compensation - CD&A (often by reference to proxy)
    #     ],
    #     "directions": "Assess management's track record, tenure, insider ownership, and whether compensation structure (from the CD&A) is aligned with long-term shareholder value rather than short-term metrics.",
    # }
    # CAP_ALLOC = {
    #     "name": "Capital allocation",
    #     "locations": [
    #         TenKSection.PART_II_ITEM_7,     # MD&A - capital allocation priorities discussion
    #         TenKSection.PART_II_ITEM_8,     # Cash Flow Statement - financing activities (buybacks, dividends, debt issuance/repayment)
    #         TenKSection.PART_III_ITEM_11,   # Executive Compensation - CD&A tying compensation to capital-return metrics (often by reference to proxy)
    #         TenQSection.PART_I_ITEM_1,      # Cash Flow Statement - financing activities
    #     ],
    #     "directions": "Review the historical mix of dividends, buybacks, debt paydown, and reinvestment/M&A to judge whether management deploys capital rationally and at sensible valuations, rather than by habit or empire-building.",
    # }
    # BALANCE_SHEET = {
    #     "name": "Balance sheet resilience",
    #     "locations": [
    #         TenKSection.PART_II_ITEM_7,     # MD&A - liquidity discussion and credit facility availability
    #         TenKSection.PART_II_ITEM_8,     # Balance Sheet / Notes - assets, liabilities, equity, debt footnote (maturity schedule, covenants, rates)
    #         TenQSection.PART_I_ITEM_1,      # Balance Sheet - assets, liabilities, and equity
    #     ],
    #     "directions": "Evaluate leverage levels, debt maturity schedule, and covenant headroom to determine how well the company could withstand a downturn or refinancing stress without diluting shareholders.",
    # }
    # INDUSTRY_STRUCT = {
    #     "name": "Industry structure",
    #     "locations": [
    #         TenKSection.PART_I_ITEM_1,      # Business - industry overview and competitive landscape
    #         TenKSection.PART_I_ITEM_1A,     # Risk Factors - industry-specific risks (cyclicality, regulation, disruption)
    #         TenKSection.PART_II_ITEM_7,     # MD&A - industry trend and macro commentary
    #     ],
    #     "directions": "Characterize the industry's competitive intensity, concentration, cyclicality, and regulatory exposure to understand the structural backdrop the company operates within, independent of company-specific performance.",
    # }
    # ACCOUNTING_STANDARDS = {
    #     "name": "Accounting standards",
    #     "locations": [
    #         TenKSection.PART_II_ITEM_8,     # Notes - Significant Accounting Policies, Recent Accounting Pronouncements, Critical Audit Matters
    #     ],
    #     "directions": "Note any aggressive, unusual, or frequently-changing accounting policies, and flag critical audit matters that suggest judgment-heavy or contentious areas of the financial statements.",
    # }
