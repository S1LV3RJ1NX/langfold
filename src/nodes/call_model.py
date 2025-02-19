from langchain_core.runnables import RunnableConfig
from src.models.state import AgentState
from src.services.llm import MODEL


async def call_model(
    state: AgentState,
    config: RunnableConfig,
):
    response = await MODEL.ainvoke(state["messages"], config)
    return {"messages": [response]}
