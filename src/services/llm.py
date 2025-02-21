# TODO: Implement a service for the LLM
from langchain_openai import ChatOpenAI
from src.tools import TOOLS
from src.config import settings

MODEL = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    base_url=settings.LITELLM_GATEWAY_URL,
    api_key=settings.LITELLM_GATEWAY_API_KEY,
)

# Note: Do not forget to reassign the model to the variable
MODEL = MODEL.bind_tools(TOOLS)
