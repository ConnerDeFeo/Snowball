import urllib.error

from utils import analysis_client

# Standard SEC 8-K item titles, keyed by item number.
ITEM_TITLES = {
    "1.01": "Entry into a Material Definitive Agreement",
    "1.02": "Termination of a Material Definitive Agreement",
    "1.03": "Bankruptcy or Receivership",
    "1.04": "Mine Safety",
    "1.05": "Material Cybersecurity Incidents",
    "2.01": "Completion of Acquisition or Disposition of Assets",
    "2.02": "Results of Operations and Financial Condition",
    "2.03": "Creation of a Direct Financial Obligation",
    "2.04": "Triggering Events That Accelerate a Financial Obligation",
    "2.05": "Costs Associated with Exit or Disposal Activities",
    "2.06": "Material Impairments",
    "3.01": "Notice of Delisting or Failure to Satisfy a Listing Rule",
    "3.02": "Unregistered Sales of Equity Securities",
    "3.03": "Material Modification to Rights of Security Holders",
    "4.01": "Changes in Registrant's Certifying Accountant",
    "4.02": "Non-Reliance on Previously Issued Financial Statements",
    "5.01": "Changes in Control of Registrant",
    "5.02": "Departure/Election of Directors or Officers; Compensatory Arrangements",
    "5.03": "Amendments to Articles of Incorporation or Bylaws",
    "5.04": "Temporary Suspension of Trading Under Employee Benefit Plans",
    "5.05": "Amendments to the Code of Ethics",
    "5.07": "Submission of Matters to a Vote of Security Holders",
    "5.08": "Shareholder Director Nominations",
    "6.01": "ABS Informational and Computational Material",
    "7.01": "Regulation FD Disclosure",
    "8.01": "Other Events",
    "9.01": "Financial Statements and Exhibits",
}


# "Item 2.02" -> "Item 2.02 Results of Operations and Financial Condition"
def _item_label(item: str) -> str:
    number = item.removeprefix("Item").strip()
    title = ITEM_TITLES.get(number)
    return f"Item {number} {title}" if title else f"Item {number}"


# One line per cached 8-K in the year range (newest first): id | dates | items.
def eight_k_list(tckr: str, start_year: int, end_year: int) -> str:
    lines = []
    for m in analysis_client.list_events(tckr, start_year, end_year):
        items = "; ".join(_item_label(i) for i in m.get("items", [])) or "(no items detected)"
        lines.append(f"{m['id']} | filed {m['filing_date']} | event {m.get('date_of_report')} | {items}")
    return "\n".join(lines) or "(no 8-Ks cached)"


def read_8k(tckr: str, event_id: str) -> str:
    try:
        return analysis_client.get_event(tckr, event_id)["markdown"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "8-K not found"
        raise
