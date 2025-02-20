from langchain_core.runnables import RunnableConfig
from src.models.state import AgentState


async def should_continue(state: AgentState, config: RunnableConfig):
    """
    Determines whether the agent should continue processing based on the last message in the state.

    This function checks the last message in the agent's state to see if it contains any tool calls.
    If tool calls are present, it indicates that the agent should transition to a tool node for further processing.
    If no tool calls are found, the function indicates that the agent has reached the end of its processing.

    Args:
        state (AgentState): The current state of the agent, which includes a list of messages.
        config (RunnableConfig): Configuration settings that may influence the decision-making process.

    Returns:
        str: A string indicating the next step for the agent:
             - "tool_node" if the last message contains tool calls,
             - "end" if there are no tool calls present.
    """
    # Extract the list of messages from the agent's state
    messages = state["messages"]

    # Get the last message from the list of messages
    last_message = messages[-1]

    # Check if the last message contains any tool calls
    if last_message.tool_calls:
        # If tool calls are present, return "tool_node" to indicate the next processing step
        return "tool_node"
    else:
        # If no tool calls are found, return "end" to indicate that processing should stop
        return "end"
