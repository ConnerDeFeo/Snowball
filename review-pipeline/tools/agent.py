# tools/agent.py
from langchain_aws import ChatBedrock
from langchain.agents import create_agent
from langchain_core.tools import tool
from tools.fetch_rationale import fetch_rationale

# ... build manifest, rend_dateer to string as `manifest_text`
# ... table, ticker, start_date, end_date as before
def run_agent(tckr:str, start_date:str, end_date:str, manifest_text:str, user_text:str):

    # Agent reads the docstring
    @tool
    def get_rationale(section: str) -> str:
        """Get the full reasoning and supporting quotes behind a section's score.
        Use the section name exactly as it appears in the manifest."""
        item = fetch_rationale(tckr, start_date, end_date, section)
        return str(item) if item else "no rationale found for that section"

    llm = ChatBedrock(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0", region_name="us-east-2")
    agent = create_agent(
        model=llm,
        tools=[get_rationale],
        system_prompt=(
            "You answer questions about a company's analysis.\n\n"
            f"Scores for {tckr}, {start_date}-{end_date}:\n{manifest_text}\n\n"
            "Call get_rationale for the reasoning behind any score. "
            "Use section names exactly as written above."
        ),
    )

    result = agent.invoke({"messages": [{"role": "user", "content": user_text}]})
    return result