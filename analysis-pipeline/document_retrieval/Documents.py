from edgar import Company, set_identity, CompanyNotFoundError
from dotenv import load_dotenv
import os
import FormType

# Set identity for EDGAR db
load_dotenv()
identity = os.environ.get("EDGAR_IDENTITY")
set_identity(identity)

class Documents:
    def __init__(self, company: Company):
        self.company = company

    @classmethod
    def create(cls, tckr):
        try:
            company = Company(tckr)
        except CompanyNotFoundError:
            return None
        return cls(company)

    def _get_relevant_year(self, year: str, filings: object):
        if len(filings) > 1:
            # disambiguate — e.g. prefer the one whose period_of_report matches `year`
            filings = [f for f in filings if f.period_of_report.startswith(str(year))]
        return filings[0].obj() if filings else None

    def fetch_10k(self, year: int):
        
        filings = self.company.get_filings(form=FormType.TEN_K.value, amendments=False, year=year)
        if filings.empty:
            return None
        return self._get_relevant_year(year, filings)

    def fetch_multiple_10k(self, from_date: str, to_date: str):
        filings = self.company.get_filings(form="10-K").filter(date=f"{from_date}:{to_date}")

        for filing in filings:
            print(filing.filing_date, filing.accession_number)


    def fetch_10q(self, year: int, quarter: int):
        """Fetch a specific 10-Q by fiscal year and quarter (1-4)."""

        filings = self.company.get_filings(form=FormType.TEN_Q.value, amendments=False, year=year, quarter=quarter)
        if filings.empty:
            return None

        return self._get_relevant_year(year, filings)


    def fetch_proxy(self, year: int):
        """Fetch a specific DEF 14A proxy statement by year."""

        filings = self.company.get_filings(form=FormType.PROXY.value, year=year)
        if filings.empty:
            return None

        return self._get_relevant_year(year, filings)
    
documents = Documents.create("AAPL")

documents.fetch_multiple_10k("2020-01-01:2024-12-31")