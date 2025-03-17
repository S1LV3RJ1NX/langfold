from langchain_openai import ChatOpenAI
from src.tools import TOOLS
from src.config import settings

# Initialize base model
MODEL = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    base_url=settings.LITELLM_GATEWAY_URL,
    api_key=settings.LITELLM_GATEWAY_API_KEY,
)

# Model with tools bound
TOOL_ENABLED_MODEL = MODEL.bind_tools(TOOLS)
