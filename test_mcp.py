"""
Test script to interact with the MCP server directly
"""
import asyncio
from fastmcp import Client


async def test_mcp_server():
    """Test the MCP server tools and resources"""
    
    # Connect to MCP server
    mcp_url = "http://localhost:8000/mcp/sse"
    
    print("🔗 Connecting to MCP server...")
    async with Client(mcp_url) as client:
        
        # List available tools
        print("\n📋 Available Tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # List available resources
        print("\n📚 Available Resources:")
        resources = await client.list_resources()
        for resource in resources:
            print(f"  - {resource.uri}: {resource.name}")
        
        # List available prompts
        print("\n💬 Available Prompts:")
        prompts = await client.list_prompts()
        for prompt in prompts:
            print(f"  - {prompt.name}: {prompt.description}")
        
        # Test the generate_marketing_plan tool
        print("\n🚀 Testing generate_marketing_plan tool...")
        result = await client.call_tool(
            "generate_marketing_plan",
            arguments={
                "user_message": "Create a brief marketing plan for a new eco-friendly water bottle",
                "history": "[]"
            }
        )
        
        print("\n✅ Marketing Plan Generated:")
        print("-" * 60)
        print(result.content[0].text)
        print("-" * 60)
        
        # Test reading a resource
        print("\n📖 Reading system prompt resource...")
        resource = await client.read_resource("prompt://system")
        print(resource.contents[0].text[:200] + "...")
        
        print("\n✅ All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
