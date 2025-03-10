from src.config import Settings
from src.services.agents.custom_react_agent import run_custom_react_agent
from src.services.agents.standard_react_agent import run_react_agent


async def run_agent(thread_id: str, user_input: str):
    """
    Asynchronously runs the agent's workflow based on user input.

    This function takes a thread ID and user input, constructs the necessary
    configuration and input messages, and processes them through the agent's
    graph. It streams events generated during the processing and collects
    them for further handling.

    Args:
        thread_id (str): Unique identifier for the conversation thread.
        user_input (str): The input message from the user to be processed.

    Returns:
        dict: A dictionary containing the AI's response.
    """
    agent_type = Settings().AGENT_CONFIG.get("type")

    match agent_type:
        case "custom_react_agent":
            return await run_custom_react_agent(thread_id, user_input)
        case "react_agent":
            return await run_react_agent(user_input)
        case _:
            raise ValueError(f"Invalid agent type: {agent_type}")
