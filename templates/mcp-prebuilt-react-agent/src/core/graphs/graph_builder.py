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
from src.tools import TOOLS
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from src.config import settings
from src.utils.logger import logger
from src.utils.checkpointer_factory import CheckpointerFactory


class MCPClientManager:
    """
    Manager for MCP client sessions.

    This class ensures that MCP client sessions stay open during the entire
    lifecycle of the agent's operation.
    """

    _instance = None
    _client = None
    _tools = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MCPClientManager, cls).__new__(cls)
            cls._instance._server_configs = {}
        return cls._instance

    async def initialize(self):
        """Initialize the MCP client with server configurations."""
        if self._client is not None:
            return

        server_configs = settings.AGENT_CONFIG.get("mcp_servers", [])

        # for server_path in server_paths:
        for server_config in server_configs:
            server_type = server_config.get("type")
            if server_type == "python":
                server_path = server_config.get("path")
                server_name = server_config.get("name")
                abs_path = os.path.abspath(server_path.replace(".", "/") + ".py")
                logger.info(f"Setting up MCP server: {server_name} at {abs_path}")

                self._server_configs[server_name] = {
                    "command": "python",
                    "args": [abs_path],
                    "transport": "stdio",
                }
            elif server_type == "url":
                server_name = server_config.get("name")
                url = server_config.get("url")
                self._server_configs[server_name] = {
                    "url": url,
                    "transport": "sse",
                }

        # Initialize the client
        self._client = MultiServerMCPClient(self._server_configs)
        await self._client.__aenter__()
        self._tools = self._client.get_tools()
        logger.info("MCP client initialized successfully")

    async def close(self):
        """Close the MCP client session."""
        if self._client is not None:
            await self._client.__aexit__(None, None, None)
            self._client = None
            self._tools = None
            logger.info("MCP client closed")

    @property
    def tools(self):
        """Get the tools from the MCP client."""
        if self._tools is None:
            raise ValueError("MCP client not initialized")
        return self._tools


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
        self.mcp_client_manager = MCPClientManager()

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

            try:
                # Initialize the MCP client manager
                await instance.mcp_client_manager.initialize()

                # Get the tools from the MCP client manager
                mcp_tools = instance.mcp_client_manager.tools

                # Combine MCP tools with local tools
                if TOOLS:
                    tools = [*mcp_tools, *TOOLS]
                else:
                    tools = mcp_tools

                # Compile the graph with checkpointing
                instance._graph = create_react_agent(
                    model=MODEL,
                    tools=tools,
                    prompt=prompt,
                    checkpointer=instance.checkpointer,
                )
                logger.info("Graph compiled successfully with MCP tools")
            except Exception as e:
                logger.error(f"Error compiling graph: {e}")
                # Make sure to close the MCP client on error
                await instance.mcp_client_manager.close()
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
