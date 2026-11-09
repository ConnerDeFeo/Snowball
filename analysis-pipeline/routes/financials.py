from fastapi import APIRouter

from financials.read_statements import read_statements

router = APIRouter()


# Reads cached financial statements for every 10-K/10-Q in the year range.
@router.get("/financials/{tckr}")
def get_financials_route(tckr: str, start_year: int, end_year: int):
    return read_statements(tckr, start_year, end_year)
