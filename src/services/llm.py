# TODO: Implement a service for the LLM

import os
from langchain_openai import ChatOpenAI
from src.tools import TOOLS

MODEL = ChatOpenAI(
    model="openai-main/gpt-4o-mini",
    temperature=0,
    base_url=os.getenv("LLM_GATEWAY_URL"),
    api_key=os.getenv("TFY_API_KEY"),
)

# Note: Do not forget to reassign the model to the variable
MODEL = MODEL.bind_tools(TOOLS)
