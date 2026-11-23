# tools/agent.py
import json
from typing import Awaitable, Callable, Optional

from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk
from langchain_core.tools import tool
from filings.eight_k import eight_k_list, read_8k as fetch_8k
from filings.grep_filing import grep_filing
from filings.manifest import filings_manifest
from filings.proxy import grep_proxy, read_proxy as fetch_proxy
from filings.read_section import read_section as fetch_section
from tools.tool_log import format_log, record_call, record_result
from utils import analysis_client
from utils.llm import DEFAULT_EFFORT, DEFAULT_MODEL, chat_model

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
    # every request, so only user/assistant turns are kept. Each assistant turn ends
    # with a compact [Tools used this turn] log (calls + short digests, not full results).
    history: Optional[list[dict]] = None,
    # Callable function that takes dict param and returns awaitable nothing
    on_progress: Optional[Callable[[dict], Awaitable[None]]] = None,
    model: str = DEFAULT_MODEL,
    effort: str = DEFAULT_EFFORT,
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
    def grep_filing_tool(form: str, year: str, quarter: str, pattern: str) -> str:
        """Regex-search (case-insensitive) every section of one filing at once. Use form,
        year and quarter exactly as in the filings manifest (quarter is an empty string
        for a 10-K). Returns matches with surrounding context, each labeled with the
        section it came from. Use this to find WHERE something is mentioned, then
        read_section to read that section."""
        result = grep_filing(tckr, form, year, quarter or None, pattern)
        return result if result is not None else "filing not found (it may need to be re-fetched)"

    @tool
    def grep_proxy_tool(proxy_id: str, pattern: str) -> str:
        """Regex-search (case-insensitive) one proxy statement (DEF 14A). Use proxy_id exactly
        as it appears on the DEF 14A lines of the filings manifest. Returns matches with
        surrounding context, each labeled with its character offset. Pass an offset to
        read_proxy to read more of the passage."""
        result = grep_proxy(tckr, proxy_id, pattern)
        return result if result is not None else "proxy not found (it may need to be re-fetched)"

    @tool
    def read_proxy(proxy_id: str, offset: int) -> str:
        """Read about 8,000 characters of one proxy statement (DEF 14A), starting just before
        the character offset (use an offset from grep_proxy_tool). The result ends with the
        range returned and the total length; pass the end of that range as offset to continue."""
        result = fetch_proxy(tckr, proxy_id, offset)
        return result if result is not None else "proxy not found (it may need to be re-fetched)"

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
    def list_8k_filings() -> str:
        """List this company's 8-K current reports in the year range, newest first: id,
        filing date, event date, and the 8-K items (what each filing is about, e.g.
        earnings results, officer changes, acquisitions). Pass an id to read_8k."""
        try:
            return eight_k_list(tckr, start_year, end_year)
        except Exception as e:
            return f"could not list 8-Ks: {e}"

    @tool
    def read_8k(event_id: str) -> str:
        """Read the full text of one 8-K (primary document plus exhibits such as the
        press release). Use the id exactly as shown by list_8k_filings."""
        try:
            return fetch_8k(tckr, event_id)
        except Exception as e:
            return f"could not read 8-K: {e}"

    @tool
    def fetch_filings() -> str:
        """Download this company's 10-K/10-Q/proxy/8-K filings for the year range from SEC EDGAR.
        Call this first if the filings manifest is empty. Returns the updated manifest."""
        try:
            result = analysis_client.fetch_documents(tckr, start_year, end_year)
        except Exception as e:
            return f"could not fetch filings: {e}"
        if result.get("type") == "error":
            return f"could not fetch filings: {result.get('detail')}"
        return filings_manifest(tckr, start_year, end_year) or "(no sections found after fetching)"

    agent = create_agent(
        model=chat_model(model, effort),
        tools=[read_section, grep_filing_tool, grep_proxy_tool, read_proxy, get_evidence, list_8k_filings, read_8k, fetch_filings],
        system_prompt=(
            f"You answer questions about {tckr}'s SEC filings ({start_year}-{end_year}).\n\n"
            f"Sections the user mentioned (full text, may be empty):\n{mentions_text or '(none)'}\n\n"
            f"Cached filings (year filed | form | period or proxy id, then section):\n{filings_manifest_text or '(none cached)'}\n\n"
            f"Checklist questions ([id] text):\n{checklist_manifest_text}\n\n"
            "Answer from the mentioned sections first. Call read_section to read any other "
            "section in the filings manifest (use year/form/period/section exactly as written there). "
            "If you don't know which section mentions something, call grep_filing_tool to regex-search a whole "
            "filing, then read_section on the section it points to. "
            "For executive pay, board, governance or shareholder-vote questions, call grep_proxy_tool "
            "on a DEF 14A from the manifest, then read_proxy at a hit's offset. "
            "Call get_evidence for the evidence behind a checklist question. "
            "For material events (earnings releases, executive changes, acquisitions, etc.) call "
            "list_8k_filings to browse the 8-Ks, then read_8k on the relevant ones. "
            "If the filings manifest is empty, call fetch_filings before answering. "
            "Cite the form, year and section you relied on. "
            "When you rely on figures from a tool result, state them explicitly in your answer. "
            "Earlier assistant turns end with a [Tools used this turn] log. That log is only a short digest "
            "of each result. You saw the full results when you wrote that answer, so quotes and figures in "
            "your earlier answers are verified. Don't re-check, doubt or retract them just because they "
            "don't appear in the digest. Re-call a tool only to read new material, or if the user disputes a specific claim."
        ),
    )

    if on_progress:
        await on_progress({"type": "start"})

    messages = (history or []) + [{"role": "user", "content": user_text}]

    # Stream node-by-node updates so we can report each tool call as it happens,
    # and collect the text of every assistant message (including text written before a tool call).
    segments: list[str] = []
    log: list[dict] = []
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
                for call in tool_calls:
                    record_call(log, call)
                    if on_progress:
                        await on_progress({"type": "progress", "tool": call["name"], "args": call.get("args", {})})
                if getattr(msg, "type", None) == "tool":
                    record_result(log, msg)
                if getattr(msg, "type", None) == "ai":
                    text = _text_of(msg.content).strip()
                    if text:
                        segments.append(text)

    final_text = "\n\n".join(segments)
    # The tool log goes only into stored history, not the answer returned to the user.
    stored_text = final_text
    if log:
        stored_text += f"\n\n[Tools used this turn (results truncated; the answer above was written from the full results):\n{format_log(log)}]"
    updated_history = messages + [{"role": "assistant", "content": stored_text}]
    return final_text, updated_history
