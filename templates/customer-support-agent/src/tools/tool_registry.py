from pathlib import Path
from importlib import import_module
from inspect import getmembers
from langchain_core.tools import BaseTool

from src.config import settings
from src.utils.logger import logger


def auto_register_tools():
    """
    Automatically register tools specified in the configuration.

    This function:
    1. Retrieves tool specifications from the configuration
    2. Dynamically imports and registers the tools from Python modules

    Tools are agent-agnostic and can be used with any agent type.

    Returns:
        tuple: A tuple containing:
            - tools (list): A list of registered tool instances.
            - tools_by_name (dict): A dictionary mapping tool names to their instances.
    """
    # Get the configuration from settings

    # Initialize collections for registered tools
    tools = []
    tools_by_name = {}
    for config_name, config in settings.AGENT_CONFIGS.items():

        # Get tool specifications from the configuration
        tool_specs = config.get("tools", [])

        # Create a set of tool names for efficient lookup
        tool_names = {tool_spec["name"] for tool_spec in tool_specs}

        if not tool_names:
            logger.warning(
                "No tools specified in configuration. No tools will be registered."
            )
            return [], {}

        logger.info(f"Registering tools: {tool_names}")

        # Path to the tools directory
        tools_dir = Path(__file__).parent

        # Dynamically import and register tools
        for file in tools_dir.glob("*.py"):
            if file.name in ["__init__.py", "tool_registry.py"]:
                continue  # Skip initialization files

            module_name = f"src.tools.{file.stem}"
            try:
                # Import the module
                module = import_module(module_name)

                # Find BaseTool instances in the module
                for _, obj in getmembers(module):
                    if isinstance(obj, BaseTool) and obj.name in tool_names:
                        tools.append(obj)
                        tools_by_name[obj.name] = obj
                        logger.debug(f"Registered tool: {obj.name}")
            except ImportError as e:
                logger.error(f"Error importing {module_name}: {e}")

        # Log summary of registered tools
        if tools:
            logger.info(f"Successfully registered {len(tools)} tools")
        else:
            logger.warning("No tools were registered")

    return tools, tools_by_name
