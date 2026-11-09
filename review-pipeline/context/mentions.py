from filings.read_section import read_section

# Renders the sections the user @-mentioned as full text for the system prompt.
def render_mentions(tckr: str, mentions: list[dict]) -> str:
    blocks = []
    for m in mentions:
        quarter = m.get("quarter")
        label = f"{m['form']} {m['year']}{' ' + quarter if quarter else ''} {m['section']}"
        text = read_section(tckr, m["form"], m["year"], quarter, m["section"])
        blocks.append(f"=== {label} ===\n{text if text is not None else 'not found'}")
    return "\n\n".join(blocks)
