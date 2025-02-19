# Note: This file will always be there
from src.services.graph_builder import GRAPH
from src.utils.chat import print_event, get_ai_response


async def run_agent(thread_id: str, user_input: str):

    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("user", user_input)]}

    events = []
    async for event in GRAPH.astream(inputs, config=config, stream_mode="values"):
        print_event(event)
        events.append(event)

    response = await get_ai_response(events)
    return {"response": response}
