# Custom React Agent Implementation Guide

## Overview

The Custom React Agent provides a more flexible and powerful implementation that allows for complex workflows, conditional branching, and fine-grained control over tool execution. It's built using LangGraph's graph-based architecture.

## When to Use Custom React Agent

Choose the Custom React Agent when:

- You need complex decision-making logic
- You want fine-grained control over tool execution flow
- You need conditional branching based on tool results
- You're building a sophisticated agent with multiple decision paths

## Architecture

```mermaid
graph TD
    A[User Input] --> B[Call Model Node]
    B --> C{Should Continue?}
    C -->|Yes| D[Tool Node]
    D --> B
    C -->|No| E[End]

    subgraph "Node Details"
        F[Call Model Node]
        F --> G[Process Input]
        G --> H[Generate Tool Calls]
        H --> I[Generate Response]
    end
```

## Configuration

To use the Custom React Agent, configure your `agent.yaml` as follows:

```yaml
type: "custom_react_agent"
prompt: >-
  You are a helpful AI assistant designed to provide clear, accurate, and relevant responses.
  When answering questions:
  1. If you need more information, ask clarifying questions
  2. Break down complex topics into simpler explanations
  3. Provide specific examples when helpful
  4. Acknowledge if you're unsure about something
  5. Focus on addressing the core of the user's question

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
  - name: tool_name
    description: "Description of what the tool does"
    arguments:
      type: object
      properties:
        arg1:
          type: string

checkpointer:
  type: "redis"
  kwargs:
    max_connections: 10
```

## Implementation Details

### Core Components

1. **Nodes**

   - `call_model`: Processes input and generates responses/tool calls
   - `tool_node`: Executes tools and processes results
   - `should_continue`: Determines if more actions are needed

2. **Edges**

   - Define the flow between nodes
   - Support conditional routing based on node outputs

3. **Graph Structure**

   - Built using LangGraph's StateGraph
   - Maintains conversation state throughout execution

4. **Checkpointer**
   - Used to save and restore agent state
   - Supports in-memory or redis backend

### Flow

1. User input enters through the entry point
2. Call Model node processes input
3. Should Continue node evaluates next action
4. Tool Node executes tools if needed
5. Process repeats until completion
