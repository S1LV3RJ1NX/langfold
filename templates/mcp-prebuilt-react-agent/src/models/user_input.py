# NOTE: This file will always be there
from pydantic import BaseModel


class UserInput(BaseModel):
    """
    UserInput is a Pydantic model that represents the input provided by a user in a specific thread.

    This model is used to validate and serialize user input data, ensuring that the required fields
    are present and correctly formatted. It inherits from Pydantic's BaseModel, which provides
    built-in validation and parsing capabilities.

    Attributes:
        thread_id (str): A unique identifier for the thread in which the user input is being provided.
                         This helps in organizing and managing conversations or interactions.

        user_input (str): The actual input text provided by the user. This field captures the user's
                          message or query that needs to be processed by the system.
    """

    thread_id: str  # Unique identifier for the conversation thread
    user_input: str  # The input text from the user
