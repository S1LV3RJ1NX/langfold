from langchain_core.messages import AIMessage


def print_event(event):
    """
    Prints the last message from the event if available.

    This function retrieves the 'messages' from the provided event dictionary.
    If messages are present, it checks if they are in a list format. If so, it
    selects the last message and calls its pretty_print method to display it.

    Args:
        event (dict): A dictionary containing event data, expected to have a
                      'messages' key that holds a list of message objects.
    """
    message = event.get("messages", [])
    if message:
        if isinstance(message, list):
            message = message[-1]  # Select the last message if it's a list
        message.pretty_print()  # Print the message in a formatted way


async def get_ai_response(events):
    """
    Retrieves the AI response from a list of events.

    This asynchronous function processes a list of events in reverse order to find
    the last AI message that does not involve tool calls. It extracts the content
    of the message, which can be in various formats (string, list, or dictionary),
    and returns it as a single string. If an error occurs during this process,
    the error message is returned instead.

    Args:
        events (list): A list of event dictionaries, each potentially containing
                       a 'messages' key with a list of message objects.

    Returns:
        str or None: The content of the last AI message as a string, or None if no
                     valid message is found.
    """
    for event in reversed(events):  # Process events in reverse order
        if event.get("messages"):  # Check if there are messages in the event
            last_message = event["messages"][-1]  # Get the last message
            if isinstance(last_message, AIMessage) and not last_message.tool_calls:
                try:
                    content = last_message.content  # Extract the content of the message
                    if isinstance(content, str):
                        return content  # Return string content directly
                    elif isinstance(content, list):
                        # Flatten the list of content and join into a single string
                        return " ".join(
                            [str(item) for sublist in content for item in sublist]
                        )
                    elif isinstance(content, dict):
                        # Join string values from the dictionary into a single string
                        return " ".join(
                            [str(v) for k, v in content.items() if isinstance(v, str)]
                        )
                    else:
                        return str(content)  # Convert other types to string
                except Exception as e:
                    return str(e)  # Return the error message as a string

    return None  # Return None if no valid message is found
