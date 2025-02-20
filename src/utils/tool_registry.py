from pathlib import Path
from importlib import import_module
from inspect import getmembers, isfunction
from src.utils.logger import logger
from langchain_core.tools import BaseTool


def auto_register_tools():
    """Automatically register all functions decorated with @tool in the tools directory."""
    tools = []
    tools_by_name = {}

    # Path to the tools directory
    tools_dir = Path(__file__).parent.parent / "tools"

    logger.debug(f"Tools directory: {tools_dir}")

    # Iterate through all Python files in the tools directory
    for file in tools_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue

        # Import the module
        module_name = f"src.tools.{file.stem}"
        try:
            module = import_module(module_name)

            # Find all functions in the module
            for name, obj in getmembers(module):
                # Check if the object is a BaseTool instance
                if isinstance(obj, BaseTool):
                    tools.append(obj)
                    tools_by_name[obj.name] = obj
                    logger.debug(f"Registered tool: {obj.name}")
        except ImportError as e:
            print(f"Error importing {module_name}: {e}")

    return tools, tools_by_name
