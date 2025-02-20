from pathlib import Path
from importlib import import_module
from inspect import getmembers
from langchain_core.tools import BaseTool

from src.utils.logger import logger


def auto_register_tools():
    """
    Automatically register all functions decorated with @tool in the tools directory.

    This function scans the 'tools' directory for Python files, imports each module,
    and checks for any functions that are instances of BaseTool. It collects these
    tools into a list and a dictionary for easy access by name.

    Returns:
        tuple: A tuple containing:
            - tools (list): A list of registered tool instances.
            - tools_by_name (dict): A dictionary mapping tool names to their instances.
    """
    tools = []  # List to hold registered tool instances
    tools_by_name = {}  # Dictionary to map tool names to their instances

    # Path to the tools directory, which is two levels up from this file
    tools_dir = Path(__file__).parent.parent / "tools"

    logger.debug(f"Tools directory: {tools_dir}")  # Log the tools directory path

    # Iterate through all Python files in the tools directory
    for file in tools_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue  # Skip the __init__.py file

        # Construct the module name based on the file name
        module_name = f"src.tools.{file.stem}"
        try:
            # Dynamically import the module
            module = import_module(module_name)

            # Find all functions in the module using getmembers
            for name, obj in getmembers(module):
                # Check if the object is an instance of BaseTool
                if isinstance(obj, BaseTool):
                    tools.append(obj)  # Add the tool to the list
                    tools_by_name[obj.name] = obj  # Map the tool's name to its instance
                    logger.debug(
                        f"Registered tool: {obj.name}"
                    )  # Log the registration of the tool
        except ImportError as e:
            # Log an error message if the module cannot be imported
            logger.error(f"Error importing {module_name}: {e}")

    return tools, tools_by_name  # Return the list and dictionary of registered tools
