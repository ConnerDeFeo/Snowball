# tools/agent.py
from langchain_aws import ChatBedrock
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from fetch_rationale import fetch_rationale

# ... build manifest, render to string as `manifest_text`
# ... table, ticker, start, end as before
def run_agent(tckr, start, end, manifest_text):

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

    llm = ChatBedrock(model_id="...", region_name="us-east-2")
    executor = AgentExecutor(
        agent=create_tool_calling_agent(llm, [get_rationale], prompt),
        tools=[get_rationale],
        verbose=True,
    )

    return executor.invoke({"input": "why is the revenue durability score what it is?"})