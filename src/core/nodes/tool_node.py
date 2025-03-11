import json
from src.models.state import AgentState
from langchain_core.messages import ToolMessage
from src.tools import TOOLS_BY_NAME


async def tool_node(state: AgentState):
    """
    Asynchronously processes tool calls from the agent's state and invokes the corresponding tools.

    This function retrieves the last message from the agent's state, checks for any tool calls,
    and invokes the specified tools with the provided arguments. The results of the tool invocations
    are then formatted into ToolMessage objects and returned.

    Args:
        state (AgentState): The current state of the agent, which includes a list of messages.
                            The last message is expected to contain tool calls.

    Returns:
        dict: A dictionary containing a list of ToolMessage objects under the 'messages' key.
              Each ToolMessage represents the result of a tool invocation.
    """
    # Initialize an empty list to store the results of tool invocations
    outputs = []

    # Iterate over each tool call present in the last message of the state
    for tool_call in state["messages"][-1].tool_calls:
        # Asynchronously invoke the tool specified by the tool call name with the provided arguments
        tool_result = await TOOLS_BY_NAME[tool_call["name"]].ainvoke(tool_call["args"])

        # Create a ToolMessage object to encapsulate the result of the tool invocation
        outputs.append(
            ToolMessage(
                content=json.dumps(
                    tool_result
                ),  # Convert the tool result to a JSON string
                name=tool_call["name"],  # Name of the tool being invoked
                tool_call_id=tool_call["id"],  # Unique identifier for the tool call
            )
        )

    # Return the results wrapped in a dictionary under the 'messages' key
    return {"messages": outputs}
