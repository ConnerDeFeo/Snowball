import asyncio

from grading.constants.rubric_directions import RUBRIC_DIRECTIONS
from grading.grade_category import grade_category
from grading.types.GradedTimePeriod import GradedTimePeriod


async def _grade_all(tckr: str, start_date: str, end_date: str) -> list[GradedTimePeriod]:
    tasks = [
        asyncio.to_thread(grade_category, tckr, category, start_date, end_date)
        for category in RUBRIC_DIRECTIONS
    ]
    return await asyncio.gather(*tasks)


def grade_company(tckr: str, start_date: str, end_date: str) -> list[GradedTimePeriod]:
    return asyncio.run(_grade_all(tckr, start_date, end_date))
