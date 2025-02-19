# TODO: Auto build graph from yaml
from langgraph.graph import StateGraph, END, START
from src.models import AgentState
from langgraph.checkpoint.memory import MemorySaver

from src.nodes import call_model, should_continue, tool_node


# Define a new graph
workflow = StateGraph(AgentState)

# Define the nodes
workflow.add_node(tool_node)
workflow.add_node(call_model)


workflow.add_edge(START, "call_model")
# We now add a conditional edge
workflow.add_conditional_edges(
    "call_model", should_continue, {"tool_node": "tool_node", "end": END}
)
workflow.add_edge("tool_node", "call_model")

# TODO: Replace with a redis checkpointer
memory_checkpointer = MemorySaver()

GRAPH = workflow.compile(checkpointer=memory_checkpointer)
