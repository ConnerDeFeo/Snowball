from utils import analysis_client

# Lists every checklist question with its id, so the agent can fetch evidence by id.
def get_checklist_manifest() -> str:
    lines = []
    for category in analysis_client.get_checklist():
        lines.append(category["name"])
        lines += [f"  [{q['id']}] {q['text']}" for q in category["questions"]]
    return "\n".join(lines)
