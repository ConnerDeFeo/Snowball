# utils/finding_key.py
# Shared helpers for parsing snowball_findings sort keys:
#   year#form#period#rubric_category#section#version#model_id
# version is a compound "v{primary}-v{secondary}", e.g. "v1-v2".

def split_key(finding_key: str) -> list[str]:
    return finding_key.split("#")

def version_sort_key(finding_key: str) -> tuple[int, int, str]:
    parts = split_key(finding_key)
    version, model_id = parts[5], parts[6]
    primary, secondary = version.split("-")
    return (int(primary.lstrip("v")), int(secondary.lstrip("v")), model_id)
