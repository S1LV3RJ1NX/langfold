import json
from src.models.state import AgentState
from langchain_core.messages import ToolMessage
from src.tools import TOOLS_BY_NAME


async def tool_node(state: AgentState):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = await TOOLS_BY_NAME[tool_call["name"]].ainvoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}
