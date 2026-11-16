from edgar import Company, set_identity, CompanyNotFoundError
from dotenv import load_dotenv
import os
from enums.FormType import FormType, INSIDER_FORMS

# Set identity for EDGAR db
load_dotenv()
identity = os.environ.get("EDGAR_IDENTITY")
set_identity(identity)

# TEMPORARY DEBUG: log what SEC actually returned when edgartools raises
# "SEC returned HTML or XML content instead of expected SGML". Remove once diagnosed.
import logging
from edgar.sgml import sgml_parser

_orig_raise_html_error = sgml_parser._raise_sec_html_error

def _logged_raise_html_error(content):
    import re
    title = re.search(r"<title>(.*?)</title>", content, re.S | re.I)
    body = re.sub(r"<(script|style).*?</\1>", " ", content, flags=re.S | re.I)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    logging.getLogger(__name__).error(
        "SEC HTML response: len=%d title=%r text=%r", len(content), title and title.group(1).strip(), text[:500]
    )
    _orig_raise_html_error(content)

sgml_parser._raise_sec_html_error = _logged_raise_html_error

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

    # 8-K Retrieval (Filing objects; stored as markdown, so no .obj() parse here)
    def fetch_multiple_8k(self, start_year: int, end_year: int):
        filings = self.company.get_filings(form=FormType.EIGHT_K.value).filter(date=f"{start_year}-01-01:{end_year}-12-31")

        return list(filings)

    # Insider / ownership filings: Form 4 and 13D (old "SC" and new "SCHEDULE" names)
    def fetch_multiple_insiders(self, start_year: int, end_year: int):
        forms = [f.value for f in INSIDER_FORMS]
        filings = self.company.get_filings(form=forms).filter(date=f"{start_year}-01-01:{end_year}-12-31")

        return list(filings)