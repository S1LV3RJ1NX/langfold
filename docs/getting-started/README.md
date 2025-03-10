# Getting Started Guide

## Overview
This project provides a flexible framework for building AI agents using LangGraph. It supports two types of agents:
1. Standard React Agent - For simple, sequential workflows
2. Custom React Agent - For complex, graph-based workflows with conditional branching

## Prerequisites
- Python 3.8+
- Poetry (for dependency management)
- Basic understanding of async Python
- Familiarity with YAML configuration

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
poetry install
```

### 2. Configuration
1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Update the environment variables:
```env
LITELLM_GATEWAY_URL=your_gateway_url
LITELLM_GATEWAY_API_KEY=your_api_key
LOG_LEVEL=INFO
```

### 3. Choose Your Agent Type

#### For Simple Workflows (React Agent)
1. Create/edit `agent.yaml`:
```yaml
type: "react_agent"
prompt: >-
  You are a helpful AI assistant...
tools:
  - name: get_username
    description: "Use this tool when user asks for their username."
    arguments:
      type: object
      properties: {}
      required: []
```

#### For Complex Workflows (Custom React Agent)
1. Create/edit `agent.yaml`:
```yaml
type: "custom_react_agent"
prompt: >-
  You are a helpful AI assistant...
nodes:
  - name: tool_node
  - name: call_model
  - name: should_continue
entry_point: call_model
edges:
  - from: tool_node
    to: call_model
conditional_edges:
  - from: call_model
    condition: should_continue
    mapping:
      tool_node: tool_node
      end: END
tools:
  - name: get_username
    description: "Use this tool when user asks for their username."
    arguments:
      type: object
      properties: {}
      required: []
```

### 4. Run the Application
```bash
poetry run uvicorn src.main:app --reload
```

## Project Structure
```
.
├── src/
│   ├── core/
│   │   ├── agents/        # Agent implementations
│   │   ├── nodes/         # Graph nodes for custom agent
│   │   └── graphs/        # Graph definitions
│   ├── tools/             # Tool implementations
│   ├── models/            # Data models
│   └── utils/             # Utility functions
├── docs/
│   ├── agents/            # Agent documentation
│   ├── tools/             # Tool documentation
│   └── getting-started/   # Getting started guides
├── tests/                 # Test files
├── agent.yaml             # Agent configuration
├── poetry.lock           # Lock file for dependencies
└── pyproject.toml        # Project configuration
```

## Development Workflow

### 1. Creating a New Tool
1. Create a new file in `src/tools/`
2. Implement your tool using the `@tool` decorator
3. Add tool specification to `agent.yaml`
4. Tools are automatically registered

### 2. Testing
```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_my_feature.py
```

### 3. Code Style
```bash
# Format code
poetry run black .

# Check types
poetry run mypy .
```

## Common Tasks

### Adding a New Tool
1. Create tool file (`src/tools/my_tool.py`):
```python
from langchain_core.tools import BaseTool

@tool
async def my_tool(param: str) -> dict:
    """Tool description."""
    return {"response": f"Processed {param}"}
```

2. Add to `agent.yaml`:
```yaml
tools:
  - name: my_tool
    description: "Tool description"
    arguments:
      type: object
      properties:
        param:
          type: string
          description: "Parameter description"
      required: ["param"]
```

### Debugging
1. Set `LOG_LEVEL=DEBUG` in `.env`
2. Check logs for detailed information
3. Use the built-in debugging endpoints

## Next Steps
1. Read the detailed [React Agent Guide](../agents/react/README.md)
2. Explore the [Custom React Agent Guide](../agents/custom-react/README.md)
3. Learn about [Tool Development](../tools/README.md)

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support
- GitHub Issues: Report bugs and feature requests
- Documentation: Check the `docs/` directory
- Community: Join our Discord server
