from langchain_core.messages import AIMessage


def print_event(event):
    message = event.get("messages", [])
    if message:
        if isinstance(message, list):
            message = message[-1]
        message.pretty_print()


async def get_ai_response(events):
    for event in reversed(events):
        if event.get("messages"):
            last_message = event["messages"][-1]
            if isinstance(last_message, AIMessage) and not last_message.tool_calls:
                try:
                    content = last_message.content
                    if isinstance(content, str):
                        return content
                    elif isinstance(content, list):
                        return " ".join(
                            [str(item) for sublist in content for item in sublist]
                        )
                    elif isinstance(content, dict):
                        return " ".join(
                            [str(v) for k, v in content.items() if isinstance(v, str)]
                        )
                    else:
                        return str(content)
                except Exception as e:
                    return str(e)

    return None
