from fastapi import APIRouter

from utils.dynamo import companies_table

router = APIRouter()


@router.get("/companies")
def list_companies():
    items = companies_table.scan_all()
    items.sort(key=lambda item: item.get("last_graded_at", ""), reverse=True)
    return [
        {
            "ticker": item["tckr"],
            "start_year": int(item["start_year"]),
            "end_year": int(item["end_year"]),
        }
        for item in items
    ]
