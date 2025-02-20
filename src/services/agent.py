# NOTE: This file will always be there
from src.services.graph_builder import GRAPH
from src.utils.chat import print_event, get_ai_response


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

    # Configuration for the agent, including the thread ID
    config = {"configurable": {"thread_id": thread_id}}

    # Input messages formatted for the agent's processing
    inputs = {"messages": [("user", user_input)]}

    # List to store events generated during the processing
    events = []

    # Asynchronously stream events from the agent's graph
    async for event in GRAPH.astream(inputs, config=config, stream_mode="values"):
        # Print the event to the console or log
        print_event(event)
        # Append the event to the events list for further processing
        events.append(event)

    # Get the AI's response based on the collected events
    response = await get_ai_response(events)

    # Return the response in a structured format
    return {"response": response}
