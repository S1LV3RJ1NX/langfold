from src.config import Settings
import importlib

# Cache for imported agent functions
_AGENT_CACHE = {}


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

    # Try to get from cache first
    if agent_type in _AGENT_CACHE:
        agent_function = _AGENT_CACHE[agent_type]
    else:
        # Map agent types to their module paths and function names
        agent_modules = {
            "custom_react_agent": (
                "src.core.agents.custom_react_agent",
                "run_custom_react_agent",
            ),
            "react_agent": ("src.core.agents.standard_react_agent", "run_react_agent"),
        }

        if agent_type not in agent_modules:
            raise ValueError(
                f"Invalid agent type: {agent_type}. Available types: {list(agent_modules.keys())}"
            )

        module_path, function_name = agent_modules[agent_type]

        # Dynamically import the module
        module = importlib.import_module(module_path)
        agent_function = getattr(module, function_name)

        # Cache for future use
        _AGENT_CACHE[agent_type] = agent_function

    # Call with appropriate arguments based on the agent type explicitly
    if agent_type == "react_agent":
        return await agent_function(user_input)
    elif agent_type == "custom_react_agent":
        return await agent_function(thread_id, user_input)
    else:
        raise ValueError(
            f"Invalid agent type: {agent_type}. Available types: {list(agent_modules.keys())}"
        )
