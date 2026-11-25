
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My First MCP Server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract_numbers(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@mcp.tool()
def greet_user(name: str) -> str:
    """Greet the user"""
    return f"Hello {name}, welcome to MCP!"

if __name__ == "__main__":
    mcp.run(transport="stdio")
