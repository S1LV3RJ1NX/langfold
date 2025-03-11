# NOTE: This file will always be there
from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """
    AgentState is a subclass of MessagesState that represents the current state of the agent.

    This class inherits from MessagesState, which provides the foundational structure for managing
    the messages exchanged during the agent's operation. The AgentState class can be extended in
    the future to include additional attributes or methods specific to the agent's functionality.

    Attributes:
        messages (list): A list of messages that represent the conversation history or state of the agent.
                         This is inherited from the MessagesState class.
    """

    pass
