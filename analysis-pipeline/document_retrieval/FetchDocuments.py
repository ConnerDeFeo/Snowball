from edgar import Company, set_identity, CompanyNotFoundError
from dotenv import load_dotenv
import os
from document_retrieval.FormType import FormType

# Set identity for EDGAR db
load_dotenv()
identity = os.environ.get("EDGAR_IDENTITY")
set_identity(identity)

class FetchDocuments:
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

    # 10k Retrieval
    def fetch_10k(self, year: int):
        
        filings = self.company.get_filings(form=FormType.TEN_K.value, amendments=False, year=year)
        if filings.empty:
            return None
        return self._get_relevant_year(year, filings)

    def fetch_multiple_10k(self, start_year: int, end_year: int):
        """Return filing handles (not yet downloaded) within [start_year, end_year]."""
        filings = self.company.get_filings(form=FormType.TEN_K.value).filter(date=f"{start_year}-01-01:{end_year}-12-31")

        return list(filings)

    # 10q Retrieval
    def fetch_10q(self, year: int, quarter: int):
        """Fetch a specific 10-Q by fiscal year and quarter (1-4)."""

        filings = self.company.get_filings(form=FormType.TEN_Q.value, amendments=False, year=year, quarter=quarter)
        if filings.empty:
            return None

        return self._get_relevant_year(year, filings)
    
    def fetch_multiple_10q(self, start_year: int, end_year: int):
        """Return filing handles (not yet downloaded) within [start_year, end_year]."""
        filings = self.company.get_filings(form=FormType.TEN_Q.value).filter(date=f"{start_year}-01-01:{end_year}-12-31")

        return list(filings)

    # Proxy Retrieval
    def fetch_proxy(self, year: int):
        """Fetch a specific DEF 14A proxy statement by year."""

        filings = self.company.get_filings(form=FormType.PROXY.value, year=year)
        if filings.empty:
            return None

        return self._get_relevant_year(year, filings)
    
    def fetch_multiple_proxy(self, start_year: int, end_year: int):
        # Proxy statements are stored as raw text (Filing.text()), not the
        # compensation-focused object .obj() would return, so we return the
        # Filing objects themselves here.
        filings = self.company.get_filings(form=FormType.PROXY.value).filter(date=f"{start_year}-01-01:{end_year}-12-31")

        return list(filings)