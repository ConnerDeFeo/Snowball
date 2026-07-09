from edgar import Company, set_identity
from dotenv import load_dotenv
import os

load_dotenv()
identity = os.environ.get("EDGAR_IDENTITY")

set_identity(identity)


def fetch_10k(tckr: str, year: int):
    company = Company(tckr)
    filings = company.get_filings(form="10-K", amendments=False, year=year)
    if filings.empty:
        return None
    if len(filings) > 1:
        # disambiguate — e.g. prefer the one whose period_of_report matches `year`
        filings = [f for f in filings if f.period_of_report.startswith(str(year))]
    return filings[0] if filings else None

filing = fetch_10k("AAPL", 2025)
tenk = filing.obj()
print("End")
print(tenk.business)
    
