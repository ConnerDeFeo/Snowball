# tools/agent.py
from typing import Awaitable, Callable, Optional

from langchain_aws import ChatBedrock
from langchain.agents import create_agent
from langchain_core.tools import tool
from tools.fetch_grade_rationale import fetch_grade_rationale
from tools.fetch_findings_rationale import fetch_findings_rationale

# ... build manifest, render to string as `manifest_text`
# ... table, ticker, start_year, end_year as before
async def run_agent(
    tckr:str, start_year:int, end_year:int, manifest_text:str, findings_manifest_text:str, user_text:str,
    # Callable function that takes dict param and returns awaitable nothing
    on_progress: Optional[Callable[[dict], Awaitable[None]]] = None,
) -> str:

    # Agent reads the docstring
    @tool
    def get_rationale(section: str) -> str:
        """Get the full reasoning and supporting quotes behind a section's score.
        Use the section name exactly as it appears in the manifest. section must be in snake_case format."""
        item = fetch_grade_rationale(tckr, start_year, end_year, section)
        return str(item) if item else "no rationale found for that section"

    @tool
    def get_finding(year: str, form: str, period: str, category: str, section: str) -> str:
        """Get the underlying finding (reasoning and supporting quotes) for a specific
        filing's rubric category and section. Use year, form, period, category, and
        section exactly as they appear in the findings manifest. category and section
        must be in snake_case format."""
        item = fetch_findings_rationale(tckr, year, form, period, category, section)
        return str(item) if item else "no finding found for that filing/category/section"

    llm = ChatBedrock(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0", region_name="us-east-2", max_tokens=4096)
    agent = create_agent(
        model=llm,
        tools=[get_rationale, get_finding],
        system_prompt=(
            "You answer questions about a company's analysis.\n\n"
            f"Scores for {tckr}, {start_year}-{end_year}:\n{manifest_text}\n\n"
            f"Findings available for {tckr}, {start_year}-{end_year} (year | form | period, "
            f"then category / section):\n{findings_manifest_text}\n\n"
            "Call get_rationale for the reasoning behind a category score (uses section names "
            "exactly as written in the scores manifest above).\n"
            "Call get_finding for the underlying finding behind a specific filing's category/section "
            "(uses year/form/period/category/section exactly as written in the findings manifest above)."
        ),
    )

    if on_progress:
        await on_progress({"type": "start"})

    # Stream node-by-node updates so we can report each tool call as it happens,
    # and keep the latest assistant text as the running answer.
    final_text = ""
    async for chunk in agent.astream({"messages": [{"role": "user", "content": user_text}]}, stream_mode="updates"):
        for update in chunk.values():
            for msg in update.get("messages", []):
                tool_calls = getattr(msg, "tool_calls", None) or []
                if on_progress:
                    for call in tool_calls:
                        await on_progress({"type": "progress", "tool": call["name"], "args": call.get("args", {})})
                if getattr(msg, "type", None) == "ai" and not tool_calls:
                    content = msg.content
                    final_text = content if isinstance(content, str) else str(content)

    return final_text