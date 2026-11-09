# Version strings are "v{n}" (e.g. "v1", "v2"), stored on each question and
# sub-agent item. Bumping invalidates the cached evidence keyed off that
# version (see evidence/evidence_cache.py).
def bump(version: str) -> str:
    n = int(version.removeprefix("v"))
    return f"v{n + 1}"
