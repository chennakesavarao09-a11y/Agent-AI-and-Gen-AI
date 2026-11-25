
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_file = Path(__file__).with_name("mcp_server.py")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("\nAvailable MCP Tools:")
            for tool in tools.tools:
                print("-", tool.name)

            operations = [
                ("add_numbers", {"a": 20, "b": 10}, "Addition"),
                ("subtract_numbers", {"a": 20, "b": 10}, "Subtraction"),
                ("multiply_numbers", {"a": 20, "b": 10}, "Multiplication"),
                ("divide_numbers", {"a": 20, "b": 10}, "Division"),
                ("greet_user", {"name": "Student"}, "Greeting")
            ]

            for tool_name, arguments, label in operations:
                result = await session.call_tool(
                    tool_name,
                    arguments=arguments
                )
                print(label + ":", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
