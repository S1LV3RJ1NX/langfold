# NOTE: This file will always be there
"""
Graph Builder module for constructing and managing the agent's workflow graph.

This module provides a singleton GraphBuilder class that constructs a directed graph
representing the agent's workflow using the langgraph library. The graph structure is
defined in the agent configuration and consists of nodes (processing steps), edges
(transitions between steps), and conditional edges (transitions based on conditions).

The graph is built once and cached for subsequent access.
"""

from langgraph.graph import StateGraph
from src.models.state import AgentState
from langgraph.checkpoint.memory import MemorySaver
from importlib import import_module

from src.config import settings
from src.utils.logger import logger
from src.core.graphs.utils import convert_special_nodes


class GraphBuilder:
    """
    Singleton class responsible for building and managing the agent's workflow graph.

    The graph is built based on configuration specified in settings.AGENT_CONFIG which defines:
    - nodes: Processing steps in the workflow
    - edges: Direct transitions between nodes
    - conditional_edges: Transitions that depend on conditions
    - entry_point: The starting node of the workflow

    Attributes:
        _instance (GraphBuilder): Singleton instance
        _graph (Graph): Compiled workflow graph
        workflow (StateGraph): Graph under construction
        agent_config (dict): Configuration for the agent's workflow
        memory_checkpointer (MemorySaver): Checkpointing mechanism for the graph
    """

    _instance = None
    _graph = None

    def __new__(cls):
        """Ensure only one instance is created (singleton pattern)"""
        if cls._instance is None:
            cls._instance = super(GraphBuilder, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the graph builder with a new StateGraph and configuration"""
        self.workflow = StateGraph(AgentState)
        self.agent_config = settings.AGENT_CONFIG
        # TODO: Add a checkpointer util
        self.memory_checkpointer = MemorySaver()

    def _add_nodes(self):
        """
        Add processing nodes to the graph from configuration.
        Each node is a Python module with a function matching the node name.
        """
        for node in self.agent_config["nodes"]:
            try:
                # Dynamically import the node's module and get its function
                module = import_module(f"src.core.nodes.{node['name']}")
                node_function = getattr(module, node["name"])
                self.workflow.add_node(node["name"], node_function)
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

    def _add_edges(self):
        """
        Add direct edges between nodes from configuration.
        Each edge represents a direct transition from one node to another.
        """
        for edge in self.agent_config["edges"]:
            try:
                self.workflow.add_edge(
                    convert_special_nodes(edge["from"]),
                    convert_special_nodes(edge["to"]),
                )
                logger.debug(f"Successfully added edge: {edge['from']} -> {edge['to']}")
            except Exception as e:
                logger.error(f"Error adding edge {edge['from']} -> {edge['to']}: {e}")
                raise

    def _add_conditional_edges(self):
        """
        Add conditional edges from configuration.
        Each conditional edge uses a condition function to determine the next node.
        """
        for cond_edge in self.agent_config["conditional_edges"]:
            try:
                # Import condition function and set up mapping of outcomes to next nodes
                module = import_module(f"src.core.nodes.{cond_edge['condition']}")
                mapping = {
                    k: convert_special_nodes(v) for k, v in cond_edge["mapping"].items()
                }
                self.workflow.add_conditional_edges(
                    convert_special_nodes(cond_edge["from"]),
                    getattr(module, cond_edge["condition"]),
                    mapping,
                )
                logger.debug(
                    f"Successfully added conditional edge from: {cond_edge['from']}"
                )
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
                logger.error(
                    f"Error adding conditional edge from {cond_edge['from']}: {e}"
                )
                raise

    def _set_entry_point(self):
        """Set the starting node for the workflow from configuration"""
        try:
            self.workflow.set_entry_point(self.agent_config["entry_point"])
            logger.debug(
                f"Successfully set entry point: {self.agent_config['entry_point']}"
            )
        except Exception as e:
            logger.error(f"Error setting entry point: {e}")
            raise

    @staticmethod
    def _build(instance):
        """
        Build and compile the workflow graph if not already built.

        Args:
            instance (GraphBuilder): The GraphBuilder instance

        Returns:
            Graph: The compiled workflow graph
        """
        if instance._graph is None:
            # Build the graph structure
            instance._add_nodes()
            instance._add_edges()
            instance._add_conditional_edges()
            instance._set_entry_point()

            try:
                # Compile the graph with checkpointing
                instance._graph = instance.workflow.compile(
                    checkpointer=instance.memory_checkpointer
                )
                logger.info("Graph compiled successfully")
            except Exception as e:
                logger.error(f"Error compiling graph: {e}")
                raise

        return instance._graph

    @classmethod
    def build(cls):
        """
        Build and return the workflow graph (entry point).

        Returns:
            Graph: The compiled workflow graph
        """
        instance = cls()
        return cls._build(instance)


# Initialize and export the singleton graph instance
GRAPH = GraphBuilder.build()
