from langchain_core.runnables import RunnableConfig
from src.models.state import AgentState


async def should_continue(state: AgentState, config: RunnableConfig):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    # Otherwise if there is, we continue
    else:
        return "end"
