from fastapi import APIRouter, HTTPException

from events.read_events import list_events, read_event

router = APIRouter()


# Metadata for every cached 8-K filed in the year range (newest first).
@router.get("/events/{tckr}")
def list_events_route(tckr: str, start_year: int, end_year: int):
    return list_events(tckr, start_year, end_year)


# Markdown body of one 8-K.
@router.get("/events/{tckr}/{event_id}")
def get_event_route(tckr: str, event_id: str):
    markdown = read_event(tckr, event_id)
    if markdown is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"markdown": markdown}
