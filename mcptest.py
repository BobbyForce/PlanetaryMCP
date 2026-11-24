import asyncio

from mcp import Client


async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # 1. Discover the tools
        tools = await client.list_tools()
        print("Available MCP tools:")
        for tool in tools.tools:
            print("-", tool.name)

        # 2. Call a MongoDB tool
        result = await client.call_tool("planets_with_rings", {})
        print("\nMongoDB results:")
        for block in result.content:
            print(block.text)

        # 3. Call the Redis tool
        result = await client.call_tool("get_statistics", {"key": "query_count"})
        print("\nRedis results:")
        for block in result.content:
            print(block.text)


asyncio.run(main())