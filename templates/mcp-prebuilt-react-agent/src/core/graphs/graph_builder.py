# NOTE: This file will always be there
"""
Graph Builder module for constructing and managing the agent's workflow graph.

This module provides a singleton GraphBuilder class that constructs a directed graph
representing the agent's workflow using the langgraph library. The graph structure is
defined in the agent configuration and consists of nodes (processing steps), edges
(transitions between steps), and conditional edges (transitions based on conditions).

The graph is built once and cached for subsequent access.
"""

import os
from src.core.agents.model_provider import MODEL
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

from src.config import settings
from src.utils.logger import logger
from src.utils.checkpointer_factory import CheckpointerFactory


class GraphBuilder:
    """
    Singleton class responsible for building and managing the agent's workflow graph.

    This class will use the prebuilt react agent from langgraph.prebuilt.

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
        self.agent_config = settings.AGENT_CONFIG
        self.checkpointer = None

    @classmethod
    async def get_graph(cls):
        """
        Get the initialized graph instance. If not initialized, wait for initialization.

        Returns:
            Graph: The compiled workflow graph
        """
        instance = cls()
        if instance._graph is None:
            instance._graph = await cls._build(instance)
        return instance._graph

    @staticmethod
    async def _build(instance):
        """
        Build and compile the workflow graph if not already built.

        Args:
            instance (GraphBuilder): The GraphBuilder instance

        Returns:
            Graph: The compiled workflow graph
        """
        if instance._graph is None:
            prompt = settings.AGENT_CONFIG.get("prompt", "You are a helpful assistant.")
            checkpointer_type = settings.get("checkpointer.type", "in_memory")
            checkpointer_kwargs = settings.get("checkpointer.kwargs", {})

            # Create checkpointer
            instance.checkpointer = await CheckpointerFactory.create_checkpointer(
                checkpointer_type, **checkpointer_kwargs
            )

            server_paths = settings.AGENT_CONFIG.get("mcp_servers", [])
            # Replace the path with the full absolute path
            # E.g: Given path: src.mcp_servers.math_server
            # Replace with: /Users/username/project/src/mcp_servers/math_server.py
            server_paths = [
                os.path.abspath(path.replace(".", "/") + ".py") for path in server_paths
            ]

            logger.info(f"Server paths: {server_paths}")

            server_params = StdioServerParameters(
                command="python",
                # Make sure to update to the full absolute path to your math_server.py file
                args=server_paths,
            )

            try:

                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        # Initialize the connection
                        await session.initialize()

                        # Get tools
                        tools = await load_mcp_tools(session)

                        # Compile the graph with checkpointing
                        instance._graph = create_react_agent(
                            model=MODEL,
                            tools=tools,
                            prompt=prompt,
                            checkpointer=instance.checkpointer,
                        )
                        logger.info("Graph compiled successfully")
            except Exception as e:
                logger.error(f"Error compiling graph: {e}")
                raise

        return instance._graph

    @classmethod
    async def build(cls):
        """
        Build and return the workflow graph (entry point).

        Returns:
            Graph: The compiled workflow graph
        """
        instance = cls()
        return await cls._build(instance)


GRAPH = None
