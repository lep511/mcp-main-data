import asyncio
import os

from fastmcp import Client

async def test_server():
    # Get the base URL from environment variable
    base_url = os.getenv("GOOGLE_RUN_URL")
    if not base_url:
        raise ValueError("GOOGLE_RUN_URL environment variable is not set")
    
    # Construct the MCP endpoint URL
    mcp_url = f"{base_url.rstrip('/')}/mcp/"
    print(mcp_url)
    
    # Test the MCP server using streamable-http transport.
    # Use "/sse" endpoint if using sse transport.
    async with Client(mcp_url) as client:
        # List available tools
        tools = await client.list_tools()
        for tool in tools:
            print(f">>> Tool found: {tool.name}")
        # Call add tool
        print(">>>  Calling add tool for 1 + 2")
        result = await client.call_tool("add", {"a": 1, "b": 2})
        print(f"<<<  Result: {result[0].text}")
        # Call subtract tool
        print(">>>  Calling subtract tool for 10 - 3")
        result = await client.call_tool("subtract", {"a": 10, "b": 3})
        print(f"<<< Result: {result[0].text}")

if __name__ == "__main__":
    asyncio.run(test_server())