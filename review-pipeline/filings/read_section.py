from botocore.exceptions import ClientError

from utils.s3 import retrieve

# Mirrors the key layout written by analysis-pipeline/document_retrieval/get_documents.py:
#   filings/{tckr}/10-K/{year}/{section}.txt
#   filings/{tckr}/10-Q/{year}/{quarter}/{section}.txt
def section_key(tckr: str, form: str, year: str, quarter: str | None, section: str) -> str:
    middle = f"{year}/{quarter}" if quarter else year
    return f"filings/{tckr}/{form}/{middle}/{section}.txt"

# Returns None if that filing/section isn't cached.
def read_section(tckr: str, form: str, year: str, quarter: str | None, section: str) -> str | None:
    try:
        return retrieve(section_key(tckr, form, year, quarter, section)).decode("utf-8")
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise
