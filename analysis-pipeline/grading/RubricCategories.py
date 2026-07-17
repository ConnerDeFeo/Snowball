from enum import Enum

### THIS IS A STANDIN FOR NOW, FURTHER RESEARCH WILL BE DONE EXTENSIVLEY LATER ON ALL AREAS

class RubricCategories(Enum):
    REVENUE_DURABILITY = {
        "name": "Revenue durability",
        "locations": [
            "10-K Item 1 (Business) - contract structure, recurring vs. project-based revenue, backlog",
            "10-K Notes to Financial Statements - Revenue Recognition footnote (ASC 606 disaggregation)",
            "10-K Item 7 (MD&A) - revenue drivers and disaggregation discussion",
        ],
        "directions": "Determine what share of revenue is contractual, recurring, or subscription-based versus one-time or project-based, and how much visibility management has into future revenue (backlog, deferred revenue, remaining performance obligations).",
    }
    REVENUE_QUALITY = {
        "name": "Revenue quality",
        "locations": [
            "10-K Notes - Revenue Recognition footnote (timing of recognition, contract assets/liabilities)",
            "10-K Item 7 (MD&A) - discussion of one-time items, divestiture gains, or channel stuffing risk",
            "10-Q - quarter-over-quarter revenue trend and any restatements or catch-up adjustments",
        ],
        "directions": "Assess whether reported revenue reflects real cash-backed demand versus aggressive recognition timing, non-recurring gains, or channel-stuffing, using the recognition footnote and any MD&A caveats.",
    }
    CUSTOMER_CONCENTRATION = {
        "name": "Customer concentration",
        "locations": [
            "10-K Item 1 (Business) - major customers disclosure (any customer >10% of revenue)",
            "10-K Notes - segment/customer concentration footnote",
            "10-K Item 1A (Risk Factors) - customer dependency risk language",
        ],
        "directions": "Identify whether revenue is concentrated in a small number of customers and note any disclosed loss-of-customer risk, contract renewal terms, or dependency language that signals fragility.",
    }
    SUPPLIER_CONCENTRATION = {
        "name": "Supplier concentration",
        "locations": [
            "10-K Item 1 (Business) - supply chain and sourcing description",
            "10-K Item 1A (Risk Factors) - single-source or key supplier dependency risk",
            "10-K Item 7 (MD&A) - commentary on input cost or supply disruption",
        ],
        "directions": "Determine how dependent the company is on a limited number of suppliers or single-source components, and whether management discloses substitutability or long-term supply agreements that mitigate that risk.",
    }
    GROSS_MARGIN = {
        "name": "Gross margin level",
        "locations": [
            "10-K / 10-Q Income Statement - gross profit line",
            "10-K Item 7 (MD&A) - gross margin discussion and drivers",
            "10-K Notes - segment footnote for margin by segment/product line",
        ],
        "directions": "Record the current gross margin level and compare it against segment or product-line detail to see whether the reported figure is being propped up or dragged down by a particular business line.",
    }
    GROSS_MARGIN_STABILITY = {
        "name": "Gross margin stability",
        "locations": [
            "10-K Item 7 (MD&A) - multi-year margin trend commentary",
            "Multiple 10-Qs - quarter-over-quarter margin trend",
            "10-K Notes - pricing, input cost, or mix-shift discussion affecting margin",
        ],
        "directions": "Track gross margin across recent quarters and years to assess volatility, and read management's explanation for swings (pricing power, input costs, product mix) to judge whether the margin is structurally stable.",
    }
    MOAT = {
        "name": "Competitive moat / ROIC persistence",
        "locations": [
            "10-K Item 1 (Business) - competitive strengths / competitive advantages section",
            "10-K Item 1A (Risk Factors) - competition risk language",
            "Historical 10-Ks (multi-year) - ROIC/ROIC-driver trend (operating income, invested capital)",
        ],
        "directions": "Evaluate management's stated competitive advantages against historical evidence of sustained high returns on invested capital, since a durable moat should show up as persistence rather than a single strong year.",
    }
    CAPITAL_BURDENS = {
        "name": "Capital intensity & reinvestment burden",
        "locations": [
            "10-K / 10-Q Cash Flow Statement - capital expenditures line",
            "10-K Item 7 (MD&A) - Liquidity and Capital Resources section",
            "10-K Notes - Property, Plant & Equipment footnote",
        ],
        "directions": "Compare capex to revenue and operating cash flow to gauge how much of earnings must be reinvested just to maintain the business, distinguishing maintenance capex from growth capex where disclosed.",
    }
    EARNINGS_QUALITY = {
        "name": "Earnings quality / cash conversion",
        "locations": [
            "10-K / 10-Q Cash Flow Statement - reconciliation of net income to operating cash flow",
            "10-K Item 7 (MD&A) - non-GAAP reconciliation and adjustments discussion",
            "10-K Notes - reserves, accruals, and allowance for doubtful accounts footnotes",
        ],
        "directions": "Check how closely net income converts into operating cash flow over time, and scan for large or growing gaps driven by accruals, reserve releases, or non-GAAP adjustments that could flatter reported earnings.",
    }
    MANAGEMENT = {
        "name": "Management",
        "locations": [
            "Proxy Statement - executive officer and director biographies",
            "Proxy Statement - Compensation Discussion & Analysis (CD&A)",
            "10-K Item 10 (Directors, Executive Officers) - often incorporated by reference to the proxy",
        ],
        "directions": "Assess management's track record, tenure, insider ownership, and whether compensation structure (from the CD&A) is aligned with long-term shareholder value rather than short-term metrics.",
    }
    CAP_ALLOC = {
        "name": "Capital allocation",
        "locations": [
            "10-K / 10-Q Cash Flow Statement - financing activities (buybacks, dividends, debt issuance/repayment)",
            "10-K Item 7 (MD&A) - capital allocation priorities discussion",
            "Proxy Statement - CD&A section tying compensation to capital-return metrics",
        ],
        "directions": "Review the historical mix of dividends, buybacks, debt paydown, and reinvestment/M&A to judge whether management deploys capital rationally and at sensible valuations, rather than by habit or empire-building.",
    }
    BALANCE_SHEET = {
        "name": "Balance sheet resilience",
        "locations": [
            "10-K / 10-Q Balance Sheet - assets, liabilities, and equity",
            "10-K Notes - Debt footnote (maturity schedule, covenants, interest rates)",
            "10-K Item 7 (MD&A) - liquidity discussion and credit facility availability",
        ],
        "directions": "Evaluate leverage levels, debt maturity schedule, and covenant headroom to determine how well the company could withstand a downturn or refinancing stress without diluting shareholders.",
    }
    INDUSTRY_STRUCT = {
        "name": "Industry structure",
        "locations": [
            "10-K Item 1 (Business) - industry overview and competitive landscape",
            "10-K Item 1A (Risk Factors) - industry-specific risks (cyclicality, regulation, disruption)",
            "10-K Item 7 (MD&A) - industry trend and macro commentary",
        ],
        "directions": "Characterize the industry's competitive intensity, concentration, cyclicality, and regulatory exposure to understand the structural backdrop the company operates within, independent of company-specific performance.",
    }
    ACCOUNTING_STANDARDS = {
        "name": "Accounting standards",
        "locations": [
            "10-K Notes - Summary of Significant Accounting Policies",
            "10-K Notes - Recent Accounting Pronouncements / new standards adopted",
            "10-K Report of Independent Registered Public Accounting Firm - Critical Audit Matters",
        ],
        "directions": "Note any aggressive, unusual, or frequently-changing accounting policies, and flag critical audit matters that suggest judgment-heavy or contentious areas of the financial statements.",
    }