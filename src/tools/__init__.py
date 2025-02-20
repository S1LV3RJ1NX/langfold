from src.utils.tool_registry import auto_register_tools

# TOOLS: List of BaseTool instances
# TOOLS_BY_NAME: Dictionary of tool names and their corresponding BaseTool instances
TOOLS, TOOLS_BY_NAME = auto_register_tools()
