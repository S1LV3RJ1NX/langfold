import yaml
from langgraph.graph import StateGraph
from src.models.state import AgentState
from langgraph.checkpoint.memory import MemorySaver
from importlib import import_module


from src.config import settings
from src.utils.logger import logger
from src.utils.graph import convert_special_nodes

# Initialize graph
workflow = StateGraph(AgentState)
GRAPH = None

agent_config = settings.AGENT_CONFIG

# Add nodes dynamically
for node in agent_config["nodes"]:
    try:
        module = import_module(f"src.nodes.{node['name']}")
        node_function = getattr(module, node["name"])
        workflow.add_node(node["name"], node_function)
        logger.debug(f"Successfully added node: {node['name']}")
    except ModuleNotFoundError as e:
        logger.error(f"Node module not found: {node['name']}. Error: {e}")
        raise
    except AttributeError as e:
        logger.error(
            f"Node function/class not found in module: {node['name']}. Error: {e}"
        )
        raise
    except Exception as e:
        logger.error(f"Error adding node {node['name']}: {e}")
        raise

# Add edges
for edge in agent_config["edges"]:
    try:
        workflow.add_edge(
            convert_special_nodes(edge["from"]),
            convert_special_nodes(edge["to"]),
        )
        logger.debug(f"Successfully added edge: {edge['from']} -> {edge['to']}")
    except Exception as e:
        logger.error(f"Error adding edge {edge['from']} -> {edge['to']}: {e}")
        raise

# Add conditional edges
for cond_edge in agent_config["conditional_edges"]:
    try:
        module = import_module(f"src.nodes.{cond_edge['condition']}")
        mapping = {k: convert_special_nodes(v) for k, v in cond_edge["mapping"].items()}
        workflow.add_conditional_edges(
            convert_special_nodes(cond_edge["from"]),
            getattr(module, cond_edge["condition"]),
            mapping,
        )
        logger.debug(f"Successfully added conditional edge from: {cond_edge['from']}")
    except ModuleNotFoundError as e:
        logger.error(
            f"Condition module not found: {cond_edge['condition']}. Error: {e}"
        )
        raise
    except AttributeError as e:
        logger.error(
            f"Condition function/class not found in module: {cond_edge['condition']}. Error: {e}"
        )
        raise
    except Exception as e:
        logger.error(f"Error adding conditional edge from {cond_edge['from']}: {e}")
        raise

# Set entry point
try:
    workflow.set_entry_point(agent_config["entry_point"])
    logger.debug(f"Successfully set entry point: {agent_config['entry_point']}")
except Exception as e:
    logger.error(f"Error setting entry point: {e}")
    raise

# TODO: Replace with a redis checkpointer
memory_checkpointer = MemorySaver()

try:
    GRAPH = workflow.compile(checkpointer=memory_checkpointer)
    logger.info("Graph compiled successfully")
except Exception as e:
    logger.error(f"Error compiling graph: {e}")
    raise
