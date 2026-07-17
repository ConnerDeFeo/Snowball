"""Turn an edgartools ProxyStatement (filing.obj() for a DEF 14A) into a
JSON-serializable dict, grouped by data tier."""

import math
from datetime import date, datetime


def _safe(fn):
    """Call a zero-arg lambda, returning its result or None on any failure.
    Not every company tags every dimension (e.g. individual exec data), so
    field access is best-effort."""
    try:
        return fn()
    except Exception:
        return None


def _jsonable(value):
    """Coerce a single cell value (numpy/pandas/Decimal/NaN/Timestamp/etc.)
    into something json.dumps can handle."""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if hasattr(value, "item"):  # numpy scalar
        return value.item()
    if hasattr(value, "isoformat"):  # pandas Timestamp
        return value.isoformat()
    return value


def _df(df):
    """Serialize a DataFrame to a list of JSON-safe dict records."""
    if df is None or df.empty:
        return []
    records = df.to_dict(orient="records")
    return [{k: _jsonable(v) for k, v in row.items()} for row in records]


def build_proxy_data(proxy) -> dict:
    return {
        "metadata": {
            "form": _safe(lambda: proxy.form),
            "filing_date": _safe(lambda: _jsonable(proxy.filing_date)),
            "fiscal_year_end": _safe(lambda: _jsonable(proxy.fiscal_year_end)),
            "company_name": _safe(lambda: proxy.company_name),
            "cik": _safe(lambda: proxy.cik),
            "accession_number": _safe(lambda: proxy.accession_number),
        },
        "executive_compensation": {
            "peo_name": _safe(lambda: proxy.peo_name),
            "peo_total_comp": _safe(lambda: proxy.peo_total_comp),
            "peo_actually_paid_comp": _safe(lambda: proxy.peo_actually_paid_comp),
            "neo_avg_total_comp": _safe(lambda: proxy.neo_avg_total_comp),
            "neo_avg_actually_paid_comp": _safe(lambda: proxy.neo_avg_actually_paid_comp),
            "has_individual_executive_data": _safe(lambda: proxy.has_individual_executive_data),
            "executive_compensation": _safe(lambda: _df(proxy.executive_compensation)),
            "named_executives": _safe(lambda: _df(proxy.named_executives)),
        },
        "pay_vs_performance": {
            "total_shareholder_return": _safe(lambda: proxy.total_shareholder_return),
            "peer_group_tsr": _safe(lambda: proxy.peer_group_tsr),
            "net_income": _safe(lambda: proxy.net_income),
            "company_selected_measure": _safe(lambda: proxy.company_selected_measure),
            "company_selected_measure_value": _safe(lambda: proxy.company_selected_measure_value),
            "performance_measures": _safe(lambda: proxy.performance_measures),
            "pay_vs_performance": _safe(lambda: _df(proxy.pay_vs_performance)),
        },
        "governance": {
            "insider_trading_policy_adopted": _safe(lambda: proxy.insider_trading_policy_adopted),
        },
    }
