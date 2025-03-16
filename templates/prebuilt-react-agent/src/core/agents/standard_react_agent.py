from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config import Settings
from src.core.agents.model_provider import MODEL
from src.tools import TOOLS
from src.utils.chat import print_event, get_ai_response
from src.utils.logger import logger


async def run_react_agent(user_input: str):
    """
    Run the standard react agent workflow.

    Args:
        user_input (str): The input message from the user to be processed.

    Returns:
        dict: A dictionary containing the AI's response.
    """
    settings = Settings()
    prompt = settings.AGENT_CONFIG.get("prompt", "You are a helpful assistant.")
    logger.debug(f"System Prompt for React Agent: {prompt}")

    # Create the React agent
    graph = create_react_agent(model=MODEL, tools=TOOLS, prompt=prompt)

    inputs = {"messages": [("user", user_input)]}
    events = []

    async for event in graph.astream(inputs, stream_mode="values"):
        print_event(event)
        events.append(event)

    response = await get_ai_response(events)
    return {"response": response}