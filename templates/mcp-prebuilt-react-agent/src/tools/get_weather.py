from langchain_core.tools import tool


@tool
async def get_weather(location: str) -> str:
    """Use this to get weather information."""
    if any([city in location.lower() for city in ["nyc", "new york city"]]):
        return "It might be cloudy in nyc"
    elif any([city in location.lower() for city in ["sf", "san francisco"]]):
        return "It's always sunny in sf"
    else:
        return f"I am not sure what the weather is in {location}"
