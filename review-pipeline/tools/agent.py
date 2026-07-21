# tools/agent.py
from langchain_aws import ChatBedrock
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from fetch_rationale import fetch_rationale

# ... build manifest, render to string as `manifest_text`
# ... table, ticker, start, end as before
def run_agent(tckr:str, start:str, end:str, manifest_text:str, user_text:str):

    # Agent reads the docstring
    @tool
    def get_rationale(section: str) -> str:
        """Get the full reasoning and supporting quotes behind a section's score.
        Use the section name exactly as it appears in the manifest."""
        item = fetch_rationale(tckr, start, end, section)
        return str(item) if item else "no rationale found for that section"

    prompt = ChatPromptTemplate.from_messages([
        ("system",
        "You answer questions about a company's analysis.\n\n"
        f"Scores for {tckr}, {start}-{end}:\n{manifest_text}\n\n"
        "Call get_rationale for the reasoning behind any score. "
        "Use section names exactly as written above."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    llm = ChatBedrock(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0", region_name="us-east-2")
    agent = create_agent(
        model=llm,
        tools=[get_rationale],
        system_prompt=(
            "You answer questions about a company's analysis.\n\n"
            f"Scores for {tckr}, {start}-{end}:\n{manifest_text}\n\n"
            "Call get_rationale for the reasoning behind any score. "
            "Use section names exactly as written above."
        ),
    )

    result = agent.invoke({"messages": [{"role": "user", "content": user_text}]})
    return result