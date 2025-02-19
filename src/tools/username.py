from langchain_core.tools import tool


@tool
async def get_username():
    """Use this tool when user asks for their username."""
    try:
        return {"response": "John Doe"}
    except Exception as e:
        # Always return a dictionary with the error message
        return {"error": str(e)}
