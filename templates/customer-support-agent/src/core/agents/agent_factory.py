from src.utils.chat import print_event, get_ai_response
from src.core.graphs.graph_builder import GraphBuilder
from src.config import settings


async def run_agent(
    thread_id: str, user_input: str, config_name: str = settings.PRIMARY_CONFIG
):
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

    graph = await GraphBuilder.get_graphs()[config_name]
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("user", user_input)]}
    events = []

    async for event in graph.astream(inputs, config=config, stream_mode="values"):
        print_event(event)
        events.append(event)

    response = await get_ai_response(events)
    return {"response": response}
