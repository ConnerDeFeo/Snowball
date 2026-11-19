from fastapi import APIRouter

from proxies.read_proxies import read_proxies

router = APIRouter()


# Reads cached proxy statement (DEF 14A) data for every year in the range.
@router.get("/proxies/{tckr}")
def get_proxies_route(tckr: str, start_year: int, end_year: int):
    return read_proxies(tckr, start_year, end_year)
