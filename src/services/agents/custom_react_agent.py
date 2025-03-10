from src.config import Settings
from src.utils.chat import print_event, get_ai_response
from src.services.graph_builder import GRAPH
from src.utils.logger import logger


async def run_custom_react_agent(thread_id: str, user_input: str):
    """
    Run the custom react agent workflow.

    Args:
        thread_id (str): Unique identifier for the conversation thread.
        user_input (str): The input message from the user to be processed.

    Returns:
        dict: A dictionary containing the AI's response.
    """
    settings = Settings()
    prompt = settings.AGENT_CONFIG.get("prompt", "You are a helpful assistant.")
    logger.debug(f"System Prompt for React Agent: {prompt}")

    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("user", user_input), ("system", prompt)]}
    events = []

    async for event in GRAPH.astream(inputs, config=config, stream_mode="values"):
        print_event(event)
        events.append(event)

    response = await get_ai_response(events)
    return {"response": response}
