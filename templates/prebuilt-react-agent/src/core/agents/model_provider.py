from langchain_openai import ChatOpenAI
from src.tools import TOOLS
from src.config import Settings

# Initialize base model
MODEL = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    base_url=Settings().LITELLM_GATEWAY_URL,
    api_key=Settings().LITELLM_GATEWAY_API_KEY,
)

# Model with tools bound
TOOL_ENABLED_MODEL = MODEL.bind_tools(TOOLS)
