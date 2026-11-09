import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Statement key -> Financials method name.
STATEMENTS = {
    "income": "income_statement",
    "balance": "balance_sheet",
    "cashflow": "cashflow_statement",
}

# DataFrame columns that describe the row; everything else is a period column.
META_COLUMNS = {
    "concept", "label", "standard_concept", "unit", "level", "abstract",
    "dimension", "is_breakdown", "point_in_time", "balance", "weight", "preferred_sign",
}


def _value(v):
    if v is None or (not isinstance(v, str) and pd.isna(v)):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return str(v)


def _shape(df: pd.DataFrame) -> dict | None:
    if df is None or df.empty:
        return None
    columns = [c for c in df.columns if c not in META_COLUMNS]
    rows = []
    for _, r in df.iterrows():
        label = r.get("label")
        if not isinstance(label, str) or not label.strip():
            continue
        rows.append({
            "label": label.strip(),
            "level": int(r.get("level", 0) or 0),
            "abstract": bool(r.get("abstract", False)),
            "unit": r.get("unit") if isinstance(r.get("unit"), str) else None,
            "values": [_value(r[c]) for c in columns],
        })
    return {"columns": [str(c) for c in columns], "rows": rows}


# The income / balance / cash flow statements of one 10-K or 10-Q as plain
# JSON-ready dicts. A statement the filing lacks is left out; a filing with no
# XBRL data returns {}.
def build_statements(report) -> dict:
    financials = getattr(report, "financials", None)
    if financials is None:
        return {}
    result = {}
    for key, method in STATEMENTS.items():
        try:
            statement = getattr(financials, method)()
            if statement is None:
                continue
            shaped = _shape(statement.to_dataframe(view="standard", standard=False, include_unit=True))
        except Exception:
            logger.exception("could not build %s statement", key)
            continue
        if shaped:
            result[key] = shaped
    return result
