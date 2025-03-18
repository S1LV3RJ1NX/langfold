from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
async def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b


@mcp.tool()
async def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b


@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    return a - b


@mcp.tool()
async def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        return 0
    return a / b


if __name__ == "__main__":
    mcp.run(transport="stdio")
