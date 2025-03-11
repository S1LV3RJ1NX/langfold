from langgraph.graph import START, END


def convert_special_nodes(value):
    """
    Convert string representations of special graph nodes to their corresponding objects.

    This function takes a string input and checks if it matches the predefined special node
    identifiers "START" or "END". If a match is found, it returns the corresponding object
    from the langgraph library. If the input does not match either identifier, it returns
    the input value unchanged.

    Args:
        value (str): The string representation of a node, which can be "START", "END", or any other string.

    Returns:
        object: The corresponding START or END object if a match is found; otherwise, returns the input value.

    Example:
        >>> convert_special_nodes("START")
        <START object>

        >>> convert_special_nodes("END")
        <END object>

        >>> convert_special_nodes("OTHER_NODE")
        'OTHER_NODE'
    """
    if value == "START":
        return START  # Return the START object if the input is "START"
    if value == "END":
        return END  # Return the END object if the input is "END"
    return value  # Return the original value if no match is found
