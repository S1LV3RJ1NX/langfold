from langgraph.graph import START, END


def convert_special_nodes(value):
    """Convert string representations of START/END to actual objects"""
    if value == "START":
        return START
    if value == "END":
        return END
    return value
