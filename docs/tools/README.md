# Tool Configuration and Implementation Guide

## Overview
Tools are agent-agnostic components that provide specific functionalities to your agents. They can be used with any agent type (React or Custom React) and are configured through the `agent.yaml` file.

## Tool Configuration

### YAML Configuration
Tools are specified in the `tools` section of your `agent.yaml`:

```yaml
tools:
  - name: get_username
    description: "Use this tool when user asks for their username."
    arguments:
      type: object
      properties:
        # Define argument properties here
      required: []
```

### Tool Schema
Each tool configuration follows this structure:
```yaml
- name: tool_name                    # Required: Unique identifier for the tool
  description: "Tool description"     # Required: Clear description of tool's purpose
  arguments:                         # Optional: Tool's input parameters
    type: object                     # Fixed: Must be 'object'
    properties:                      # Optional: Define argument properties
      arg_name:                      # Argument name
        type: string|number|boolean  # Argument type
        description: "Description"   # Argument description
    required: ["arg_name"]          # List of required arguments
```

## Implementing a New Tool

### 1. Create a Tool File
Create a new Python file in the `src/tools` directory:

```python
from langchain_core.tools import BaseTool

@tool
async def my_custom_tool(arg1: str, arg2: int) -> dict:
    """
    Tool description that matches the YAML configuration.

    Args:
        arg1 (str): Description of arg1
        arg2 (int): Description of arg2

    Returns:
        dict: Result of the tool execution
    """
    try:
        # Tool implementation here
        result = {"response": "Tool result"}
        return result
    except Exception as e:
        return {"error": str(e)}
```

### 2. Tool Registration
Tools are automatically registered through the `auto_register_tools()` function in `src/tools/tool_registry.py`. The function:
- Scans the tools directory
- Matches tool implementations with YAML configurations
- Registers tools for use by agents

## Best Practices

### 1. Tool Design
- Keep tools focused on a single responsibility
- Make tool descriptions clear and specific
- Use meaningful argument names
- Provide comprehensive argument descriptions
- Include proper error handling

### 2. Configuration
- Use descriptive tool names
- Write clear tool descriptions
- Document all arguments thoroughly
- Specify required arguments explicitly

### 3. Implementation
- Follow async/await patterns
- Return results in dictionary format
- Include proper error handling
- Add logging for debugging
- Write unit tests for tools

## Example Tools

### 1. Simple Tool
```yaml
tools:
  - name: get_current_time
    description: "Get the current server time"
    arguments:
      type: object
      properties: {}
      required: []
```

```python
@tool
async def get_current_time() -> dict:
    """Get the current server time."""
    from datetime import datetime
    return {"response": datetime.now().isoformat()}
```

### 2. Tool with Arguments
```yaml
tools:
  - name: fetch_user_data
    description: "Fetch user data by ID"
    arguments:
      type: object
      properties:
        user_id:
          type: string
          description: "The unique identifier of the user"
      required: ["user_id"]
```

```python
@tool
async def fetch_user_data(user_id: str) -> dict:
    """
    Fetch user data by ID.

    Args:
        user_id (str): The unique identifier of the user
    """
    try:
        # Implementation here
        return {"response": f"User data for {user_id}"}
    except Exception as e:
        return {"error": str(e)}
```

## Common Patterns

### 1. Error Handling
```python
@tool
async def safe_tool() -> dict:
    try:
        # Tool implementation
        return {"response": "result"}
    except Exception as e:
        return {"error": str(e)}
```

### 2. Input Validation
```python
@tool
async def validated_tool(value: int) -> dict:
    if not isinstance(value, int) or value < 0:
        return {"error": "Invalid input: value must be a positive integer"}
    return {"response": f"Processed value: {value}"}
```

### 3. Async Operations
```python
@tool
async def async_tool() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://api.example.com') as response:
            data = await response.json()
            return {"response": data}
```

## Testing Tools

### Unit Testing Example
```python
import pytest

@pytest.mark.asyncio
async def test_my_tool():
    result = await my_custom_tool("test", 123)
    assert "response" in result
    assert isinstance(result["response"], str)
```
