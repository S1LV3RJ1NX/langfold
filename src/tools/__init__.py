# TODO: Add auto registry
from src.tools.username import get_username

TOOLS = [get_username]

TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}
