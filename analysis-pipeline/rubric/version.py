# Version strings are "v{n}" (e.g. "v1", "v2"), stored on both the META item
# and each formtype#section item. Bumping invalidates whatever cache keys off
# that version (findings cache, grade cache — see grading/finding_cache.py and
# grading/grade_store.py).
def bump(version: str) -> str:
    n = int(version.removeprefix("v"))
    return f"v{n + 1}"
