# tools/agent.py
import json
from typing import Awaitable, Callable, Optional

from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk
from langchain_core.tools import tool
from filings.manifest import filings_manifest
from filings.read_section import read_section as fetch_section
from utils import analysis_client
from utils.llm import chat_model

def _text_of(content) -> str:
    # Content is a str or a list of blocks; keep only the {"type": "text", "text": ...} ones (drops thinking).
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")


async def run_agent(
    tckr:str, start_year:int, end_year:int,
    mentions_text:str, filings_manifest_text:str, checklist_manifest_text:str, user_text:str,
    # Prior turns for this session, as plain {"role","content"} dicts. The
    # mentioned sections and manifests are re-injected into the system prompt
    # every request, so only user/assistant turns are kept — no serialized tool calls.
    history: Optional[list[dict]] = None,
    # Callable function that takes dict param and returns awaitable nothing
    on_progress: Optional[Callable[[dict], Awaitable[None]]] = None,
) -> tuple[str, list[dict]]:

    # Agent reads the docstring
    @tool
    def read_section(form: str, year: str, quarter: str, section: str) -> str:
        """Read the full text of one cached filing section. Use form, year, quarter and
        section exactly as they appear in the filings manifest. quarter is an empty
        string for a 10-K (the manifest shows FY)."""
        text = fetch_section(tckr, form, year, quarter or None, section)
        return text if text is not None else "section not found"

    @tool
    def get_evidence(question_id: str) -> str:
        """Get the evidence the checklist agent extracted from the filings for one
        checklist question. Use the question id exactly as it appears in the checklist
        manifest (the id in square brackets)."""
        try:
            return json.dumps(analysis_client.get_evidence(tckr, start_year, end_year, question_id))
        except Exception as e:
            return f"could not fetch evidence: {e}"

    @tool
    def fetch_filings() -> str:
        """Download this company's 10-K/10-Q/proxy filings for the year range from SEC EDGAR.
        Call this first if the filings manifest is empty. Returns the updated manifest."""
        try:
            result = analysis_client.fetch_documents(tckr, start_year, end_year)
        except Exception as e:
            return f"could not fetch filings: {e}"
        if result.get("type") == "error":
            return f"could not fetch filings: {result.get('detail')}"
        return filings_manifest(tckr, start_year, end_year) or "(no sections found after fetching)"

    agent = create_agent(
        model=chat_model(),
        tools=[read_section, get_evidence, fetch_filings],
        system_prompt=(
            f"You answer questions about {tckr}'s SEC filings ({start_year}-{end_year}).\n\n"
            f"Sections the user mentioned (full text, may be empty):\n{mentions_text or '(none)'}\n\n"
            f"Cached filing sections (year | form | period, then section):\n{filings_manifest_text or '(none cached)'}\n\n"
            f"Checklist questions ([id] text):\n{checklist_manifest_text}\n\n"
            "Answer from the mentioned sections first. Call read_section to read any other "
            "section in the filings manifest (use year/form/period/section exactly as written there). "
            "Call get_evidence for the evidence behind a checklist question. "
            "If the filings manifest is empty, call fetch_filings before answering. "
            "Cite the form, year and section you relied on."
        ),
    )

    if on_progress:
        await on_progress({"type": "start"})

    messages = (history or []) + [{"role": "user", "content": user_text}]

    # Stream node-by-node updates so we can report each tool call as it happens,
    # and collect the text of every assistant message (including text written before a tool call).
    segments: list[str] = []
    async for mode, data in agent.astream({"messages": messages}, stream_mode=["updates", "messages"]):
        if mode == "messages":
            # Token-level chunks from the model; forward text to the client as it arrives.
            chunk = data[0]
            if not isinstance(chunk, AIMessageChunk):  # skip tool results
                continue
            text = _text_of(chunk.content)
            if on_progress and text and not chunk.tool_call_chunks:
                await on_progress({"type": "token", "text": text})
            continue
        for update in data.values():
            for msg in update.get("messages", []):
                tool_calls = getattr(msg, "tool_calls", None) or []
                if on_progress:
                    for call in tool_calls:
                        await on_progress({"type": "progress", "tool": call["name"], "args": call.get("args", {})})
                if getattr(msg, "type", None) == "ai":
                    text = _text_of(msg.content).strip()
                    if text:
                        segments.append(text)

    final_text = "\n\n".join(segments)
    updated_history = messages + [{"role": "assistant", "content": final_text}]
    return final_text, updated_history
